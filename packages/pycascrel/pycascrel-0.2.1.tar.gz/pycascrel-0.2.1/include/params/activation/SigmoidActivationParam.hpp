#ifndef PYCASCREL_SIGMOIDACTIVATIONPARAM_HPP
#define PYCASCREL_SIGMOIDACTIVATIONPARAM_HPP

#include "params/activation/ActivationParam.hpp"

class SigmoidActivationParam : public ActivationParam {
public:
    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;
};


#endif //PYCASCREL_SIGMOIDACTIVATIONPARAM_HPP
