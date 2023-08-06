#ifndef CASCREL_MEANSQUARELOSSPARAM_HPP
#define CASCREL_MEANSQUARELOSSPARAM_HPP

#include "params/loss/LossParam.hpp"

class MeanSquareLossParam : public LossParam {
public:
    void visit(cascrel::factory::Builder& builder) const override;
};

#endif //CASCREL_MEANSQUARELOSSPARAM_HPP
