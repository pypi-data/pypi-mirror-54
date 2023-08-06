#ifndef CASCREL_DELTARULEOPTIMIZERPARAM_HPP
#define CASCREL_DELTARULEOPTIMIZERPARAM_HPP

#include "common.hpp"

#include "params/optimizers/OptimizerParam.hpp"

class DeltaRuleOptimizerParam : public OptimizerParam {
public:
    explicit DeltaRuleOptimizerParam(cascrel::Scalar learning_rate);

    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;

private:
    cascrel::Scalar mLearningRate;
};


#endif //CASCREL_DELTARULEOPTIMIZERPARAM_HPP
