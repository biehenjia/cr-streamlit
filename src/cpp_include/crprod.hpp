#pragma once
#include "crobj.hpp"

class CRprod :public CRobj {
    public: 
        CRprod(ssize_t i, size_t l);
        
        std::unique_ptr<CRobj> add(const CRobj& target) const override;
        std::unique_ptr<CRobj> mul(const CRobj& target) const override;
        std::unique_ptr<CRobj> pow(const CRobj& target) const override;

        //todo;
        std::unique_ptr<CRobj> exp() const override;
        std::unique_ptr<CRobj> ln() const override;

        std::unique_ptr<CRobj> sin() const override;
        std::unique_ptr<CRobj> cos() const override;

        void simplify() override;
        void shift(size_t index) override;
        void print_tree() const override;
        std::string genCode(size_t parent, size_t index, ssize_t place,std::string indent) const override;



        std::unique_ptr<CRobj> copy() const override;
        std::unique_ptr<CRobj> correctp(size_t nl) const;
};

