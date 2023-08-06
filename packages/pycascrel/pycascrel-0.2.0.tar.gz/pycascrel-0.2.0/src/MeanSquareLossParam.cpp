#include "params/loss/MeanSquareLossParam.hpp"

#include "loss/MeanSquareLoss.hpp"

using cascrel::loss::MeanSquareLoss;

void MeanSquareLossParam::visit(cascrel::factory::Builder& builder) const {
    builder.withLossFunction<MeanSquareLoss>();
}
