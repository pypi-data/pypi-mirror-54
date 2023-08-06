#ifndef PYCASCREL_CASCADECORRELATIONNETWORKWRAPPER_HPP
#define PYCASCREL_CASCADECORRELATIONNETWORKWRAPPER_HPP

#include "common.hpp"

#include "CascadeCorrelationNetwork.hpp"
#include "History.hpp"

class CascadeCorrelationNetworkWrapper {
public:
    explicit CascadeCorrelationNetworkWrapper(
            cascrel::CascadeCorrelationNetwork&& ccn);

    cascrel::History train(const Eigen::Ref<const cascrel::RowMatrix>& x,
                           const Eigen::Ref<const cascrel::RowMatrix>& y,
                           unsigned int patience, cascrel::Scalar tolerance,
                           unsigned int maxHidden, cascrel::Scalar maxLoss,
                           unsigned int safetyEpochLimit);

    cascrel::RowVector evaluate(const Eigen::Ref<const cascrel::RowMatrix>& x,
                                const Eigen::Ref<const cascrel::RowMatrix>& y) const;

    cascrel::RowMatrix predict(const Eigen::Ref<const cascrel::RowMatrix>& x);

    cascrel::SizeType getNumHidden() const;

    void setLogLevel(cascrel::LogLevel log_level);

private:
    cascrel::CascadeCorrelationNetwork mWrappedNetwork;
};

#endif //PYCASCREL_CASCADECORRELATIONNETWORKWRAPPER_HPP
