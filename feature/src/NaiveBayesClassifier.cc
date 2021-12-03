// FEATURE
// See COPYING and AUTHORS for copyright and license agreement terms.

// $Id: NaiveBayesClassifier.cc 1618 2014-01-15 06:01:03Z mikewong899 $

#include "NaiveBayesClassifier.h"
#include <iostream>

const bool USE_GAUSSIAN = true;

// from https://www.johndcook.com/blog/cpp_phi/
double cdf(double x)
{
    // constants
    double a1 =  0.254829592;
    double a2 = -0.284496736;
    double a3 =  1.421413741;
    double a4 = -1.453152027;
    double a5 =  1.061405429;
    double p  =  0.3275911;

    // Save the sign of x
    int sign = 1;
    if (x < 0)
        sign = -1;
    x = fabs(x)/sqrt(2.0);

    // A&S formula 7.1.26
    double t = 1.0/(1.0 + p*x);
    double y = 1.0 - (((((a5*t + a4)*t) + a3)*t + a2)*t + a1)*t*exp(-x*x);

    return 0.5*(1.0 + sign*y);
}

NaiveBayesClassifier::NaiveBayesClassifier( int _numBins, double _pPos ) {
	numBins    = _numBins;
	pPos       = _pPos;
	pNeg       = 1.0 - pPos;
	isRangeSet = false;
}

NaiveBayesClassifier::~NaiveBayesClassifier() { 
}

void NaiveBayesClassifier::setRange( double min, double max ) {
	this->min = min + FUDGE_FACTOR;
	this->max = max;
	isRangeSet = true;
}

void NaiveBayesClassifier::train( Doubles *pos, Doubles *neg ) {
	posBinCount = vector<int>( numBins );
	negBinCount = vector<int>( numBins );

	/* std::cout << "begin output" << std::endl;
	for(int i = 0; i < pos->size(); i++) {
		std::cout << (*pos)[i] << std::endl;
	}
	std::cout << "--" << std::endl;
	for(int i = 0; i < neg->size(); i++) {
		std::cout << (*neg)[i] << std::endl;
	}
	std::cout << "end output" << std::endl; */

	if( ! isRangeSet ) calculateRange( pos, neg );
	calculateBinSize();
	calculateGaussian(pos, neg);

	numPos = count( pos, posBinCount );
	numNeg = count( neg, negBinCount );

	calculateBinScores();
}

/**
 * @brief Calculate the score for each bin
 *
 * Let pBin be the probability that the property data has a value that falls within a given range.
 * Let pPos be the probability of positive protein function classification.
 *
 * Property values are clustered into discrete bins. The bins have a uniform range
 * of values. Each bin has a probability associated with it (pBin). 
 * 
 * Read variables as "Probability x given y", e.g. pBinPos is the probability
 * of bin given site. An more complete description would be: p( bin | site ) is
 * the probability of a microenvironment having a physicochemical property
 * value that falls within a given continuous range of a discrete bin, given
 * that the microenvironment characterizes a protein function to be modeled.
 *
 * pBinPos := p( bin | site )
 * pBinNeg := p( bin | ~site )
 * pBin    := p( bin )
 * pPosBin := p( pos | bin )
 **/
void NaiveBayesClassifier::calculateBinScores() {
	binScore = vector<double>( numBins );
	for( int bin = 0; bin < numBins; bin++ ) {
		double pBinPos  = ((double) posBinCount[ bin ]) / ((double) numPos);
		double pBinNeg  = ((double) negBinCount[ bin ]) / ((double) numNeg);
		double pBin     = (pBinPos * pPos) + (pBinNeg * pNeg);
		double pPosBin  = (pBinPos * pPos) / pBin;
		double minScore = log( pPos );

		if( pBin == 0.0 ) { 
			binScore[ bin ] = 0.0;
		} else { 
			double score = log( pPosBin / pPos );
			binScore[ bin ] = score < minScore ? minScore : score;
		}
	}
}

void NaiveBayesClassifier::calculateRange( Doubles *pos, Doubles *neg ) {
    min = (*pos)[0];
    max = (*pos)[0];

    Doubles::iterator iter;
    for (iter = pos->begin(); iter != pos->end(); iter++) {
        if ((*iter) > max) { max = (*iter); }
        if ((*iter) < min) { min = (*iter); }
    }
    for (iter = neg->begin(); iter != neg->end(); iter++) {
        if ((*iter) > max) { max = (*iter); }
        if ((*iter) < min) { min = (*iter); }
    }
	min += FUDGE_FACTOR;
}

void NaiveBayesClassifier::calculateGaussian( Doubles *pos, Doubles *neg) {
	double tot = 0;
	double num = 0;

	Doubles::iterator iter;
    for (iter = pos->begin(); iter != pos->end(); iter++) {
        tot += *iter;
		num += 1;
    }
    for (iter = neg->begin(); iter != neg->end(); iter++) {
        tot += *iter;
		num += 1;
    }

	mean = tot / num;

	double s = 0;
	for (iter = pos->begin(); iter != pos->end(); iter++) {
        double v = (*iter) - mean;
		s += v*v;
    }
    for (iter = neg->begin(); iter != neg->end(); iter++) {
        double v = (*iter) - mean;
		s += v*v;
    }

	stdev = sqrt(s / num);

	/* std::cout << "mean: " << mean << "stdev: " << stdev << std::endl; */
}

int NaiveBayesClassifier::count( Doubles *values, vector<int> &countBin ) {
	Doubles::iterator i;
	int bin;
	int total = 0;
	for( i = values->begin(); i != values->end(); i++ ) {
		if(USE_GAUSSIAN) {
			//std::cout << "mean: " << mean << "stdev: " << stdev << std::endl;
			if(stdev == 0) {
				// fallback to old method when no binsize
				bin = (int) (((*i) - min) / binSize);
			} else {
				double z = ((*i) - mean) / stdev;
				//std::cout << "z: " << z << std::endl; 
				double binsize = (double)1 / ((double)numBins);
				//std::cout << "binsize: " << binsize << std::endl; 
				double percentile = cdf(z);
				//std::cout << "percentile: " << percentile << std::endl; 
				bin = (int) (percentile / binsize);
				//std::cout << "bin: " << bin << std::endl; 
			}
		} else {
			bin = (int) (((*i) - min) / binSize);
		}
		if( bin < 0 )            bin = 0;
		if( bin > (numBins - 1)) bin = (numBins - 1);
		countBin[ bin ]++;
		total++;
	}
	return total;
}
