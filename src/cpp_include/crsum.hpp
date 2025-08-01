#pragma once
#include "crobj.hpp"


class CRsum : public CRobj {
    public: 
        CRsum(ssize_t i, size_t l); 
        CRsum(ssize_t i, double x, double h);
        
        std::unique_ptr<CRobj> add(const CRobj& target) const override;
        std::unique_ptr<CRobj> mul(const CRobj& target) const override;

        // handle negative power in the visitor
        std::unique_ptr<CRobj> pow(const CRobj& target) const  override;

        //covariant
        std::unique_ptr<CRobj> exp() const override;
        std::unique_ptr<CRobj> ln() const override;

        std::unique_ptr<CRobj> sin() const override;
        std::unique_ptr<CRobj> cos() const override;
        void print_tree() const override;
        void simplify() override;
        
        std::string genCode(size_t parent, size_t index, ssize_t place,std::string indent) const override;
        
        std::unique_ptr<CRobj> copy() const override;
        void shift(size_t index) override;

};