#ifndef CASCREL_SOFTPLUSACTIVATIONPARAM_HPP
#define CASCREL_SOFTPLUSACTIVATIONPARAM_HPP

#include "ActivationParam.hpp"

class SoftplusActivationParam : public ActivationParam {
public:
    void visit(cascrel::factory::Builder& builder) const override;

    void visitAlternative(cascrel::factory::Builder& builder) const override;
};

#endif //CASCREL_SOFTPLUSACTIVATIONPARAM_HPP
