#include "params/activation/SoftplusActivationParam.hpp"

#include "activation/SoftplusActivation.hpp"

using cascrel::activation::SoftplusActivation;

void SoftplusActivationParam::visit(cascrel::factory::Builder& builder) const {
    builder.withHiddenActivation<SoftplusActivation>();
}

void SoftplusActivationParam::visitAlternative(
        cascrel::factory::Builder& builder) const {
    builder.withOutputActivation<SoftplusActivation>();
}
