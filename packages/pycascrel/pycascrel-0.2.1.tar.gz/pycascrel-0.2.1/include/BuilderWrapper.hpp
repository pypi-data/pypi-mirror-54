#ifndef PYCASCREL_BUILDERWRAPPER_HPP
#define PYCASCREL_BUILDERWRAPPER_HPP

#include "common.hpp"
#include "factory/Builder.hpp"

#include "CascadeCorrelationNetworkWrapper.hpp"
#include "params/activation/ActivationParam.hpp"
#include "params/initializers/InitializerParam.hpp"
#include "params/loss/LossParam.hpp"
#include "params/optimizers/OptimizerParam.hpp"

class BuilderWrapper {
public:
    void useHiddenInitializer(const InitializerParam& p);

    void useOutputInitializer(const InitializerParam& p);

    void useHiddenOptimizer(const OptimizerParam& p);

    void useOutputOptimizer(const OptimizerParam& p);

    void useHiddenActivation(const ActivationParam& p);

    void useOutputActivation(const ActivationParam& p);

    void useLoss(const LossParam& p);

    CascadeCorrelationNetworkWrapper compile(cascrel::SizeType inputDimension,
                                             cascrel::SizeType outputDimension);

private:
    cascrel::factory::Builder mBuilder;
};

#endif //PYCASCREL_BUILDERWRAPPER_HPP
