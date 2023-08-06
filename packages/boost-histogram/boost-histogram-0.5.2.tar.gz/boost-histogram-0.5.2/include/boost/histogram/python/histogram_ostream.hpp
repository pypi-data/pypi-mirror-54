// Copyright 2018-2019 Henry Schreiner and Hans Dembinski
//
// Distributed under the 3-Clause BSD License.  See accompanying
// file LICENSE or https://github.com/scikit-hep/boost-histogram for details.

#pragma once

#include <boost/histogram/fwd.hpp>
#include <boost/histogram/python/accumulators_ostream.hpp>
#include <boost/histogram/python/axis_ostream.hpp>
#include <boost/histogram/python/storage.hpp>
#include <boost/histogram/python/sum.hpp>
#include <iosfwd>

template <class histogram_t>
bool check_empty_histogram(const histogram_t &h, bh::coverage cov) {
    using value_type = typename histogram_t::value_type;
    for(auto &&ind : bh::indexed(h, cov)) {
        if(*ind != value_type()) {
            return false;
        }
    }
    return true;
}

namespace boost {
namespace histogram {

template <typename CharT, typename Traits, typename A, typename S>
std::basic_ostream<CharT, Traits> &operator<<(std::basic_ostream<CharT, Traits> &os,
                                              const histogram<A, S> &h) {
    os << "histogram(";
    h.for_each_axis([&](const auto &a) { os << "\n  " << a << ","; });
    os << "\n  "
       << "storage=" << storage::name<S>();
    os << "\n)";

    if(!check_empty_histogram(h, bh::coverage::all)) {
        auto inner = sum_histogram(h, false);
        auto outer = sum_histogram(h, true);

        os << " # Sum: " << inner;
        if(inner != outer)
            os << " (" << outer << " with flow)";
    }
    return os;
}

} // namespace histogram
} // namespace boost
