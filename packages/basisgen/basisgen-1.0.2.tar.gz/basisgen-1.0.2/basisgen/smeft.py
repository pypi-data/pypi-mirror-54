from basisgen import (
    irrep, algebra, scalar, L_spinor, R_spinor,
    boson, fermion, Field, EFT
)

from fractions import Fraction

sm_gauge_algebra = algebra('SU3 x SU2')


def sm_irrep(highest_weight_str):
    return irrep('SU3 x SU2', highest_weight_str)


phi = Field(
    name='phi',
    lorentz_irrep=scalar,
    internal_irrep=sm_irrep('0 0 1'),
    charges=[Fraction(1, 2)],
    statistics=boson,
    dimension=1
)
phic = phi.conjugate

BL, BR = Field.strength_tensors(
    name='B',
    internal_irrep=sm_irrep('0 0 0'),
    charges=[0],
)

WL, WR = Field.strength_tensors(
    name='W',
    internal_irrep=sm_irrep('0 0 2'),
    charges=[0],
)

GL, GR = Field.strength_tensors(
    name='G',
    internal_irrep=sm_irrep('1 1 0'),
    charges=[0],
)


def Q(number_of_flavors=1):
    return Field(
        name='Q',
        lorentz_irrep=L_spinor,
        internal_irrep=sm_irrep('1 0 1'),
        charges=[Fraction(1, 6)],
        statistics=fermion,
        dimension=1.5,
        number_of_flavors=number_of_flavors
    )


def Qc(number_of_flavors=1):
    return Q(number_of_flavors).conjugate


def u(number_of_flavors=1):
    return Field(
        name='u',
        lorentz_irrep=R_spinor,
        internal_irrep=sm_irrep('1 0 0'),
        charges=[Fraction(2, 3)],
        statistics=fermion,
        dimension=1.5,
        number_of_flavors=number_of_flavors
    )


def uc(number_of_flavors=1):
    return u(number_of_flavors).conjugate


def d(number_of_flavors=1):
    return Field(
        name='d',
        lorentz_irrep=R_spinor,
        internal_irrep=sm_irrep('1 0 0'),
        charges=[-Fraction(1, 3)],
        statistics=fermion,
        dimension=1.5,
        number_of_flavors=number_of_flavors
    )


def dc(number_of_flavors=1):
    return d(number_of_flavors).conjugate


def L(number_of_flavors=1):
    return Field(
        name='l',
        lorentz_irrep=L_spinor,
        internal_irrep=sm_irrep('0 0 1'),
        charges=[-Fraction(1, 2)],
        statistics=fermion,
        dimension=1.5,
        number_of_flavors=number_of_flavors
    )


def Lc(number_of_flavors=1):
    return L(number_of_flavors).conjugate


def e(number_of_flavors=1):
    return Field(
        name='e',
        lorentz_irrep=R_spinor,
        internal_irrep=sm_irrep('0 0 0'),
        charges=[-1],
        statistics=fermion,
        dimension=1.5,
        number_of_flavors=number_of_flavors
    )


def ec(number_of_flavors=1):
    return e(number_of_flavors).conjugate


def sm_fermions(number_of_flavors):
    return [
        fermion(number_of_flavors)
        for fermion in [Q, Qc, u, uc, d, dc, L, Lc, e, ec]
    ]


sm_field_strengths = [BL, BR, WL, WR, GL, GR]

sm_scalars = [phi, phic]


def sm_field_classes(number_of_flavors=1):
    out = {}
    out.update({field: 'phi' for field in sm_scalars})
    out.update({field: 'F' for field in sm_field_strengths})
    out.update({field: 'psi' for field in sm_fermions(1)})

    return out


def smeft(number_of_flavors=1):
    return EFT(
        sm_gauge_algebra,
        sm_scalars + sm_field_strengths + sm_fermions(number_of_flavors)
    )
