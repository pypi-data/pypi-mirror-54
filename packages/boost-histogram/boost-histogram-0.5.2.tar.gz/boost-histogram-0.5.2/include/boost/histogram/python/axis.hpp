// Copyright 2018-2019 Henry Schreiner and Hans Dembinski
//
// Distributed under the 3-Clause BSD License.  See accompanying
// file LICENSE or https://github.com/scikit-hep/boost-histogram for details.

#pragma once

#include <boost/histogram/python/pybind11.hpp>

#include <boost/histogram/axis.hpp>
#include <boost/histogram/python/axis_setup.hpp>
#include <boost/histogram/python/regular_numpy.hpp>

#include <algorithm>
#include <cmath>
#include <limits>
#include <string>
#include <tuple>
#include <type_traits>
#include <vector>

namespace axis {

namespace option = bh::axis::option;

using ogrowth_t  = decltype(option::growth | option::overflow);
using uogrowth_t = decltype(option::growth | option::underflow | option::overflow);

// How edges, centers, and widths are handled
//
// We distinguish between continuous and discrete axes. The integer axis is a borderline
// case. It has disrete values, but they are consecutive. It is possible although not
// correct to treat it like a continuous axis with bin width of 1. For the sake of
// computing bin edges and bin center, we will use this ansatz here. PS: This behavior
// is already implemented in Boost::Histogram when you create an integer axis with a
// floating point value type, e.g. integer<double>. In this case, the integer axis acts
// strictly like a regular axis with a fixed bin with of 1. We don't use it here,
// because it is slightly slower than the integer<int> axis when the input values are
// truly integers.
//
// The category axis is treated like regular(size(), 0, size()) in the conversion. It is
// the responsibility of the user to set the labels accordingly when a histogram with a
// category axis is plotted.

template <class A>
struct is_integer : std::false_type {};

template <class... Ts>
struct is_integer<bh::axis::integer<int, Ts...>> : std::true_type {};

template <class A>
struct is_category : std::false_type {};

template <class U, class... Ts>
struct is_category<bh::axis::category<U, Ts...>> : std::true_type {};

template <class Continuous, class Discrete, class Integer, class A>
decltype(auto) select(Continuous &&c, Discrete &&d, Integer &&, const A &ax) {
    return bh::detail::static_if<bh::axis::traits::is_continuous<A>>(
        std::forward<Continuous>(c), std::forward<Discrete>(d), ax);
}

template <class Continuous, class Discrete, class Integer, class... Ts>
decltype(auto) select(Continuous &&,
                      Discrete &&,
                      Integer &&i,
                      const bh::axis::integer<int, Ts...> &ax) {
    return std::forward<Integer>(i)(ax);
}

/// Return bin center for continuous axis and bin value for discrete axis
template <class A>
double unchecked_center(const A &ax, bh::axis::index_type i) {
    return select([i](const auto &ax) { return ax.value(i + 0.5); },
                  [i](const auto &) { return i + 0.5; },
                  [i](const auto &ax) { return ax.value(i) + 0.5; },
                  ax);
}

/// Return bin in a native Python representation
template <class A>
decltype(auto) unchecked_bin(const A &ax, bh::axis::index_type i) {
    return bh::detail::static_if<bh::axis::traits::is_continuous<A>>(
        [i](const auto &ax) -> decltype(auto) {
            return py::make_tuple(ax.value(i), ax.value(i + 1));
        },
        [i](const auto &ax) -> decltype(auto) { return py::cast(ax.bin(i)); },
        ax);
}

template <class A>
py::array bins_impl(const A &ax, bool flow) {
    const bh::axis::index_type underflow
        = flow && (bh::axis::traits::options(ax) & option::underflow);
    const bh::axis::index_type overflow
        = flow && (bh::axis::traits::options(ax) & option::overflow);

    py::array_t<double> result(
        {static_cast<std::size_t>(ax.size() + underflow + overflow), std::size_t(2)});

    for(auto i = -underflow; i < ax.size() + overflow; ++i) {
        result.mutable_at(static_cast<std::size_t>(i + underflow), 0) = ax.value(i);
        result.mutable_at(static_cast<std::size_t>(i + underflow), 1) = ax.value(i + 1);
    }

    return std::move(result);
}

template <class... Ts>
py::array bins_impl(const bh::axis::integer<int, Ts...> &ax, bool flow) {
    const bh::axis::index_type underflow
        = flow && (bh::axis::traits::options(ax) & option::underflow);
    const bh::axis::index_type overflow
        = flow && (bh::axis::traits::options(ax) & option::overflow);

    py::array_t<int> result(static_cast<std::size_t>(ax.size() + underflow + overflow));

    for(auto i = -underflow; i < ax.size() + overflow; ++i)
        result.mutable_at(static_cast<std::size_t>(i)) = ax.value(i);

    return std::move(result);
}

template <class... Ts>
py::array bins_impl(const bh::axis::category<int, Ts...> &ax, bool flow) {
    static_assert(!(std::decay_t<decltype(ax)>::options() & option::underflow),
                  "discrete axis never has underflow");

    const bh::axis::index_type overflow
        = flow && (bh::axis::traits::options(ax) & option::overflow);

    py::array_t<int> result(static_cast<std::size_t>(ax.size() + overflow));

    for(auto i = 0; i < ax.size() + overflow; ++i)
        result.mutable_at(static_cast<std::size_t>(i)) = ax.value(i);

    return std::move(result);
}

template <class... Ts>
py::array bins_impl(const bh::axis::category<std::string, Ts...> &ax, bool flow) {
    static_assert(!(std::decay_t<decltype(ax)>::options() & option::underflow),
                  "discrete axis never has underflow");

    const bh::axis::index_type overflow
        = flow && (bh::axis::traits::options(ax) & option::overflow);

    const auto n = max_string_length(ax);
    // TODO: this should return unicode
    py::array result(py::dtype(bh::detail::cat("S", n + 1)), ax.size() + overflow);

    for(auto i = 0; i < ax.size() + overflow; i++) {
        auto sout     = static_cast<char *>(result.mutable_data(i));
        const auto &s = ax.value(i);
        std::copy(s.begin(), s.end(), sout);
        sout[s.size()] = 0;
    }

    return result;
}

/// Utility to convert bins of axis to numpy array
template <class A>
py::array bins(const A &ax, bool flow = false) {
    // this indirection is needed by pybind11
    return bins_impl(ax, flow);
}

/// Convert continuous axis into numpy.histogram compatible edge array
template <class A>
py::array_t<double> edges(const A &ax, bool flow = false, bool numpy_upper = false) {
    auto continuous = [flow, numpy_upper](const auto &ax) {
        using index_type = std::conditional_t<
            bh::axis::traits::is_continuous<std::decay_t<decltype(ax)>>::value,
            bh::axis::real_index_type,
            bh::axis::index_type>;
        const index_type underflow
            = flow && (bh::axis::traits::options(ax) & option::underflow);
        const index_type overflow
            = flow && (bh::axis::traits::options(ax) & option::overflow);

        py::array_t<double> edges(
            static_cast<std::size_t>(ax.size() + 1 + overflow + underflow));

        for(index_type i = -underflow; i <= ax.size() + overflow; ++i)
            edges.mutable_at(i + underflow) = ax.value(i);

        if(numpy_upper && !std::is_same<A, axis::regular_numpy>::value) {
            edges.mutable_at(ax.size() + underflow) = std::nextafter(
                edges.at(ax.size() + underflow), std::numeric_limits<double>::min());
        }

        return edges;
    };

    return select(
        continuous,
        [flow](const auto &ax) {
            static_assert(!(std::decay_t<decltype(ax)>::options() & option::underflow),
                          "discrete axis never has underflow");

            const bh::axis::index_type overflow
                = flow && (bh::axis::traits::options(ax) & option::overflow);

            py::array_t<double> edges(
                static_cast<std::size_t>(ax.size() + 1 + overflow));

            for(bh::axis::index_type i = 0; i <= ax.size() + overflow; ++i)
                edges.mutable_at(i) = i;

            return edges;
        },
        continuous,
        ax);
}

template <class A>
py::array_t<double> centers(const A &ax) {
    py::array_t<double> result(static_cast<std::size_t>(ax.size()));
    for(bh::axis::index_type i = 0; i < ax.size(); ++i)
        result.mutable_data()[i] = unchecked_center(ax, i);
    return result;
}

template <class A>
py::array_t<double> widths(const A &ax) {
    py::array_t<double> result(static_cast<std::size_t>(ax.size()));
    bh::detail::static_if<bh::axis::traits::is_continuous<A>>(
        [](py::array_t<double> &result, const auto &ax) {
            std::transform(ax.begin(),
                           ax.end(),
                           result.mutable_data(),
                           [](const auto &b) { return b.width(); });
        },
        [](py::array_t<double> &result, const auto &ax) {
            std::fill(result.mutable_data(), result.mutable_data() + ax.size(), 1.0);
        },
        result,
        ax);
    return result;
}

// These match the Python names except for a possible underscore
using regular_none
    = bh::axis::regular<double, bh::use_default, metadata_t, option::none_t>;
using regular_uflow
    = bh::axis::regular<double, bh::use_default, metadata_t, option::underflow_t>;
using regular_oflow
    = bh::axis::regular<double, bh::use_default, metadata_t, option::overflow_t>;
using regular_uoflow = bh::axis::regular<double, bh::use_default, metadata_t>;
using regular_uoflow_growth
    = bh::axis::regular<double, bh::use_default, metadata_t, uogrowth_t>;

using circular     = bh::axis::circular<double, metadata_t>;
using regular_log  = bh::axis::regular<double, bh::axis::transform::log, metadata_t>;
using regular_sqrt = bh::axis::regular<double, bh::axis::transform::sqrt, metadata_t>;
using regular_pow  = bh::axis::regular<double, bh::axis::transform::pow, metadata_t>;

using variable_none   = bh::axis::variable<double, metadata_t, option::none_t>;
using variable_uflow  = bh::axis::variable<double, metadata_t, option::underflow_t>;
using variable_oflow  = bh::axis::variable<double, metadata_t, option::overflow_t>;
using variable_uoflow = bh::axis::variable<double, metadata_t>;
using variable_uoflow_growth = bh::axis::variable<double, metadata_t, uogrowth_t>;

using integer_none   = bh::axis::integer<int, metadata_t, option::none_t>;
using integer_uoflow = bh::axis::integer<int, metadata_t>;
using integer_uflow  = bh::axis::integer<int, metadata_t, option::underflow_t>;
using integer_oflow  = bh::axis::integer<int, metadata_t, option::overflow_t>;
using integer_growth = bh::axis::integer<int, metadata_t, option::growth_t>;

using category_int        = bh::axis::category<int, metadata_t>;
using category_int_growth = bh::axis::category<int, metadata_t, option::growth_t>;

using category_str = bh::axis::category<std::string, metadata_t>;
using category_str_growth
    = bh::axis::category<std::string, metadata_t, option::growth_t>;

} // namespace axis

// The following list is all types supported
using axis_variant = bh::axis::variant<axis::regular_none,
                                       axis::regular_uflow,
                                       axis::regular_oflow,
                                       axis::regular_uoflow,
                                       axis::regular_uoflow_growth,
                                       axis::circular,
                                       axis::regular_log,
                                       axis::regular_pow,
                                       axis::regular_sqrt,
                                       axis::regular_numpy,
                                       axis::variable_none,
                                       axis::variable_uflow,
                                       axis::variable_oflow,
                                       axis::variable_uoflow,
                                       axis::variable_uoflow_growth,
                                       axis::integer_none,
                                       axis::integer_uflow,
                                       axis::integer_oflow,
                                       axis::integer_uoflow,
                                       axis::integer_growth,
                                       axis::category_int,
                                       axis::category_int_growth,
                                       axis::category_str,
                                       axis::category_str_growth>;

// This saves a little typing
using vector_axis_variant = std::vector<axis_variant>;
