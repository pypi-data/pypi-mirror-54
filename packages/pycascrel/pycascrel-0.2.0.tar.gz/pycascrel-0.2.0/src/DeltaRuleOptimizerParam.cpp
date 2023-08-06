#include "params/optimizers/DeltaRuleOptimizerParam.hpp"

#include "optimizers/DeltaRuleOptimizer.hpp"

using cascrel::optimizers::DeltaRuleOptimizer;

DeltaRuleOptimizerParam::DeltaRuleOptimizerParam(
        cascrel::Scalar learning_rate)
        : mLearningRate(learning_rate) {
}

void DeltaRuleOptimizerParam::visit(cascrel::factory::Builder& builder) const {
    builder.withHiddenOptimizer<DeltaRuleOptimizer>(mLearningRate);
}

void DeltaRuleOptimizerParam::visitAlternative(
        cascrel::factory::Builder& builder) const {
    builder.withOutputOptimizer<DeltaRuleOptimizer>(mLearningRate);
}
