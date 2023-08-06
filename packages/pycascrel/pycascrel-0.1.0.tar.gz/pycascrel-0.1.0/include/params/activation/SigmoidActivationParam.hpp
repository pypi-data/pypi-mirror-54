#ifndef CASCREL_SIGMOIDACTIVATIONPARAM_HPP
#define CASCREL_SIGMOIDACTIVATIONPARAM_HPP

#include "params/activation/ActivationParam.hpp"

class SigmoidActivationParam : public ActivationParam {
public:
    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;
};


#endif //CASCREL_SIGMOIDACTIVATIONPARAM_HPP
