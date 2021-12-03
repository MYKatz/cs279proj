// FEATURE
// See COPYING and AUTHORS for copyright and license agreement terms.

// $Id: NaiveBayesClassifier.h 1616 2013-12-17 00:19:09Z mikewong899 $

#ifndef BAYES_H
#define BAYES_H

#include <cmath>   // log
#include <vector>
#include "stl_types.h"
const double FUDGE_FACTOR      = -1E-5;

using std::vector;

/**
 * @brief A Naive Bayesian Network binary classifier (pos/site vs. neg/non-site) for a given Property value
 * @ingroup classification_module
 * 
 * Uniformly discretizes Property scores over a finite number of bins (typically 
 * 2 for binary values, 5 for integer or real values). Trains on the given site vs.
 * non-site values and calculates a log probability score for each bin based on the 
 * prior probability.
 **/
class NaiveBayesClassifier {
	protected:
		int            numBins;
		double         pPos;
		double         pNeg;
		double         min;
		double         max;
		double         binSize;
		double         mean;
		double         stdev;
		bool           isRangeSet;
		int            numPos;
		int            numNeg;
		vector<int>    posBinCount;
		vector<int>    negBinCount;
		vector<double> binScore;

		void calculateBinSize() { binSize = (max - min) / numBins; };
		void calculateBinScores();
		void calculateRange( Doubles *, Doubles * );
		void calculateGaussian(Doubles *, Doubles *);
		int  count( Doubles *, vector<int> & );

	public:
		NaiveBayesClassifier( int, double );
		~NaiveBayesClassifier();

		double getBinScore( int i )           { return binScore[ i ]; };
		double getBinSize()                   { return binSize; };
		double getMin()                       { return min;     };
		double getMean()                       { return mean;     };
		double getStdev()                       { return stdev;     };
		void   setRange( double, double );
		void   train( Doubles *, Doubles * );
};

#endif
