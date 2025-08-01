#include "crobj.hpp"
#include <iostream>
CRobj::CRobj(size_t l){
    length = l;
    operands.resize(l);
}

double CRobj::valueof() const{
    if (initialized){ 
        return fastvalues[0];
    }
    return 0;
}

bool CRobj::isnumber() const{
    return false;
}

double CRobj::initialize() {
    if (initialized) {
        return valueof();
    }
    initialized = true;
    fastvalues.resize(length,0);
    isnumbers.resize(length, false);

    for (size_t i = 0; i < length; i++){ 
        isnumbers[i] = operands[i]->isnumber();
        fastvalues[i] = operands[i]->initialize();
    }
    return valueof();
}

void CRobj::simplify(){
    for (size_t i = 0; i < length; i++){ 
        operands[i]->simplify();
    }
}

void CRobj::shift(size_t index) {
    return;
}

std::string CRobj::prepare(CRobj& root){

    std::string res = "";
    root.crcount ++;
    crposition = root.crcount;
    std::string temp = std::format("{}{}=[",crprefix,crposition);
    std::string delim = ",";

    for (size_t i = 0; i < operands.size(); i++){
        if (!operands[i]->isnumber()){
            res += operands[i]->prepare(root);
        }
        if (i == operands.size()-1){
            delim = "";
        }
        temp += std::format("{}{}",fastvalues[i],delim);
    }
    temp += "]\n";
    if (delim != ","){
        res += temp;
    }
    
    return res;
}

