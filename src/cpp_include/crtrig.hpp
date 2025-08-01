#pragma once 
#include "crobj.hpp"

class CRtrig : public CRobj { 
    public:
        CRtrig(ssize_t i, oc t, size_t l);

        std::unique_ptr<CRobj> add(const CRobj& target) const override;
        std::unique_ptr<CRobj> mul(const CRobj& target) const override;
        std::unique_ptr<CRobj> pow(const CRobj& target) const override;

        std::unique_ptr<CRobj> exp() const override;
        std::unique_ptr<CRobj> ln() const override;

        std::unique_ptr<CRobj> sin() const override;
        std::unique_ptr<CRobj> cos() const override;

        void simplify() override; 
        std::unique_ptr<CRobj> copy() const override;
        void shift(size_t index) override;
        // double initialize();
        double valueof() const;
        void print_tree() const override;
        std::string genCode(size_t parent, size_t index, ssize_t place,std::string indent) const override;

        oc trigtype;
        std::unique_ptr<CRobj> correctt(size_t nl) const;
        size_t index;
};