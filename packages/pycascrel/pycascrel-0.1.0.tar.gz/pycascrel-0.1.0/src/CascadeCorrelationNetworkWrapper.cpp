#include "CascadeCorrelationNetworkWrapper.hpp"

#include <utility>

#include <pybind11/pybind11.h>

using namespace cascrel;

CascadeCorrelationNetworkWrapper::CascadeCorrelationNetworkWrapper(
        CascadeCorrelationNetwork&& ccn)
        : mWrappedNetwork(std::forward<CascadeCorrelationNetwork>(ccn)) {
}

RowVector CascadeCorrelationNetworkWrapper::evaluate(
        const Eigen::Ref<const RowMatrix>& x,
        const Eigen::Ref<const RowMatrix>& y) const {
    pybind11::gil_scoped_release release;
    return mWrappedNetwork.evaluate(x, y);
}

RowMatrix CascadeCorrelationNetworkWrapper::predict(
        const Eigen::Ref<const RowMatrix>& x) {
    pybind11::gil_scoped_release release;
    return mWrappedNetwork.predict(x);
}

SizeType CascadeCorrelationNetworkWrapper::getNumHidden() const {
    return mWrappedNetwork.getNumHidden();
}

History CascadeCorrelationNetworkWrapper::train(
        const Eigen::Ref<const RowMatrix>& x,
        const Eigen::Ref<const RowMatrix>& y,
        unsigned int patience, Scalar tolerance,
        unsigned int maxHidden, Scalar maxLoss,
        unsigned int safetyEpochLimit) {
    pybind11::gil_scoped_release release;
    return mWrappedNetwork.train(x, y, patience, tolerance, maxHidden, maxLoss,
                                 safetyEpochLimit);
}

void CascadeCorrelationNetworkWrapper::setLogLevel(LogLevel log_level) {
    mWrappedNetwork.setLogLevel(log_level);
}
