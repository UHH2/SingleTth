// PDF of a dijet function for the background parametrization
// using 4 free parameters 
#include "BkgPdf4p.h" 

#include <Riostream.h>
#include <RooAbsReal.h> 
#include <RooAbsCategory.h>
#include <TMath.h>

ClassImp(BkgPdf4p); 
  
BkgPdf4p::BkgPdf4p(const char *name, const char *title, 
				   RooAbsReal& _x,
				   RooAbsReal& _p0,
				   RooAbsReal& _p1,
				   RooAbsReal& _p2,
				   RooAbsReal& _p3) :
    RooAbsPdf(name,title), 
    x("x","x",this,_x),
    p0(" p0"," p_{0}",this, _p0),
    p1(" p1"," p_{1}",this, _p1),
    p2(" p2"," p_{2}",this, _p2),
    p3(" p3"," p_{3}",this, _p3)
{ 
} 


BkgPdf4p::BkgPdf4p(const BkgPdf4p& other, const char* name) :  
  RooAbsPdf(other,name), 
  x("x", this, other.x),
  p0(" p0", this, other.p0),
  p1(" p1", this, other.p1),
  p2(" p2", this, other.p2),
  p3(" p3", this, other.p3)
{ 
} 



Double_t BkgPdf4p::evaluate() const 
{ 
  // Actual implementation

  Double_t xp = x/1000.; // scale x to TeV

  // numerator 
  Double_t num = TMath::Power(5-xp, p0);

  // denominator, 3rd order polynomial in log(x) in exponent
  Double_t d1 = p1 + p2*TMath::Log(xp) + p3*TMath::Log(xp)*TMath::Log(xp); 
  Double_t denom = TMath::Power(xp, d1); 

  // here is the result:
  Double_t result = num/denom;

  return result; 
} 




