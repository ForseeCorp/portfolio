package project1;
import java.util.Arrays;
public class Analytics {
    
	double[] array;                    //array of data points 
    int      count;
    double   sum;
    double   average;
    double   median;
    double   min;
    double   max;
    double   stdDev;
    double   mode;
    double   range;
    
    Analytics(double[] array)                                      //constructor
    {
        this.array = array;                                   //store incoming array as a reference
  
        count = count(array);
        
        
        normalize(array);                                                 //call the Normalize method
        sum(array);
        max(array);
        avg(array);
        median(array);
        min(array);
        stdDev(array);
        mode(array);
        range(array);
        
        //  --------------------------------------------------------------------------------
        // mode: method
        //--------------------------------------------------------------------------------      
        
    }
    public double mode(double[] array) {
        double mode = array[0];
        int maxCount = 0;
        for (int i = 0; i < array.length; i++) {
            double value = array[i];
            int count = 1;
            for (int j = 0; j < array.length; j++) {
                if (array[j] == value) count++;
                if (count > maxCount) {
                    mode = value;
                    maxCount = count;
                }
            }
        }
        return mode;
    }
    
    public double range (double [] array){
    	
    	range = max(array) - min(array);
    	
    	return range;
    }
    
    
    
    
    
    
    
    
    
  //  --------------------------------------------------------------------------------
 // normalize: Returns a new clean array that has all the bad/no data removed 
 //--------------------------------------------------------------------------------
     private double[] normalize(double[] array)
     {
         int i     = 0;
         int count = 0;

         for (double col : array)                    //loop through all columns                  
             if (col != Double.MIN_VALUE)            //if smallest double value (assume bad/no data)
                 count += 1;                         //add 1 to counter

         double[] array2 = new double[count];        //create a new array
         
         for (double col : array)                    //loop through array                  
             if (col != Double.MIN_VALUE)            //if not bad data
                 array2[i++] = col;                  //copy into array2                        

         return array2;                              
     }


public double getMode() {
		return mode;
	}
	public double getRange() {
		return range;
	}
//--------------------------------------------------------------------------------
//count: Count all elements of a 1 dim array
//--------------------------------------------------------------------------------
  int count(double[] array)
 {
     return array.length;                        //count = array.length                              
 }
//--------------------------------------------------------------------------------
//sum: Sum all elements of an array
//--------------------------------------------------------------------------------
  double sum(double[] array)
 {
     double total = 0;
     for (double col : array)                     //loop through all columns                  
         total += col;                            //add to total
     return total;                                
 }
//--------------------------------------------------------------------------------
//avg: Average all elements of an array
//--------------------------------------------------------------------------------
    double avg(double[] array)
 {
     int    count = count(array);                 //call count method
     double sum   = sum(array);                   //call sum method
     return sum/count;                                
 }
//--------------------------------------------------------------------------------
//median: Returns the median value on an array
//--------------------------------------------------------------------------------
     double median(double[] array)
 {    
   
     double[] array2 = Arrays.copyOf(array, array.length);   //copy the array into array2                   
     Arrays.sort(array2);                                    //sort array2
     
     int count = count(array);                   //call count method

     int mid1 = count/2;
     int mid2 = (count-1)/2;
     double median = (count%2 == 1)              //if count is odd
         ?  array2[mid1]                         //median= mid point                                                               
         : (array2[mid1] + array2[mid2]) / 2;    //median= average of 2 mid points                                                               

     return median;                              
 }
//--------------------------------------------------------------------------------
//min: Returns the minimum value within an array
//--------------------------------------------------------------------------------
    double min(double[] array)
 {
     double minimum = Double.POSITIVE_INFINITY;   //start with largest possible value
     for (double col : array)                     //loop through all columns                  
         if (col < minimum) minimum = col;        //if col is less than minimum, save it in mimimum
     return minimum;                              
 }
//--------------------------------------------------------------------------------
//max: Returns the maximum value within an array
//--------------------------------------------------------------------------------
     double max(double[] array)
 {
     double maximum = Double.NEGATIVE_INFINITY;   //start with lowest possible value
     for (double col : array)                     //loop through all columns                  
         if (col > maximum) maximum = col;        //if col is more than maximum, save it in maximum
     return maximum;                              
 }
//--------------------------------------------------------------------------------
//stdDev: Returns the standard deviation of an array
//      It is a measure of the amount of variation of a set of data values
//      Low stdDev means the values are close to the average (or are tight) 
//      1. take average of array
//      2. take the difference (delta) of each element to the average
//      3. take the square of that delta
//      4. add all those square of deltas
//      5. divide the square of deltas by count of elements
//      6. take the square root of item 5.  
//--------------------------------------------------------------------------------
     double stdDev(double[] array)
 {
     int    count   = count(array);              //call count method
     double sum     = sum(array);                //call sum method
     double average = sum/count;

     double sqDelta = 0;                         //square of deltas      
     for (double col : array)                    //loop through all columns                  
         sqDelta += Math.pow(col-average,2);     //add to square of delta

     double std_dev = Math.sqrt(sqDelta/count);  //square root of average(square of deltas)
     return std_dev;                              
 }
 
//--------------------------------------------------------------------------------
//toString: Returns the array as well as all the analytic computations 
//--------------------------------------------------------------------------------
    String toString(double[] array)
 {
     String str  = "Data points: "   + Arrays.toString(array);
            str += "\nCount......: " + count(array); 
            str += "\nSum........: " + sum(array); 
            str += "\nAverage....: " + avg(array); 
            str += "\nMedian.....: " + median(array); 
            str += "\nMinimum....: " + min(array); 
            str += "\nMaximum....: " + max(array); 
            str += "\nStd.Dev....: " + stdDev(array); 
     return str;                              
 }

//--------------------------------------------------------------------------------
//slice: Takes  a 2 dimensional array, slice type (row/col/all), and index
//     Return a single dimention array for that row or column or all cells
//--------------------------------------------------------------------------------
 static double[] slice(double[][] array2dim, String type, int idx)
 {
     int      size  = 0;
     double[] array = null;

     if (type.equals("row"))                             //ROW slice
     {
         size  = array2dim[idx].length;                      //determine the needed array size           
         array = Arrays.copyOf(array2dim[idx], size);        //copy that row into a 1dim array
     }
     if (type.equals("col"))                             //COL slice
     {           
         size  = array2dim.length;                           //determine the needed array size           
         array = new double[size];                           //create a new array of that size
         for (int i=0; i < size ; i++)                       //loop through all rows
         {
             try {                                           //try to: 
                 array[i] = array2dim[i][idx];                //copy cell from 2dim into 1dim array                     
             }
             catch (Exception e) {                           //if exception:
                 array[i] = Double.MIN_VALUE;                //cell does not exist, populate with min value
             }
         }           
     }
     if (type.equals("all"))                             //ALL slice (turn a 2dim array to 1 dim)
     {           
         for (double[] row : array2dim)                      //loop through all rows                     
             size += row.length;                             //compute the needed array size                              
         array = new double[size];                           //create a new array of that size
         int i = 0;
         for (double[] row : array2dim)                      //loop through all rows
             for (double col : row)                          //loop through all columns
                 array[i++] = col;                           //copy cell into 1dim array                         
     }

//   System.out.println(size + Arrays.toString(array));      //debug only
     return array;
 }
//--------------------------------------------------------------------------------
//transpose: Takes  a 2 dimensional array
//         Return a transposed 2 dimensional array
//--------------------------------------------------------------------------------
 static double[][] transpose(double[][] array2dim)
 {
     int rowNum  = array2dim.length;                     //compute number of rows
     int colNum  = 0;                                    //compute number of columns
         
     for (double[] row : array2dim)                      //loop through all rows                     
         if (row.length > colNum)                        //take the size of the longest row                              
             colNum = row.length;                        //this becomes the number of columns        
     
     double[][] newArray = new double[colNum][rowNum];   //create new array
                                                         //notice [row][col] dimensions are transposed
     int col2 = 0;
     for (int row=0; row < array2dim.length; row++)              //loop thru original rows
     {
         int row2 = 0;                                           
         for (int col=0; col < array2dim[row].length; col++)     //loop thru original columns
         {
             newArray[row2][col2] = array2dim[row][col];         //copy into new array           
             row2++;                                             //add 1 to row of new array
         }
         col2++;                                                 //add 1 to col of new array
     }   
     return newArray;
 }
//--------------------------------------------------------------------------------
public int getCount() {
	return count;
}
public void setCount(int count) {
	this.count = count;
}
public double getSum() {
	return sum;
}
public void setSum(double sum) {
	this.sum = sum;
}
public double getAverage() {
	return average;
}
public void setAverage(double average) {
	this.average = average;
}
public double getMedian() {
	return median;
}
public void setMedian(double median) {
	this.median = median;
}
public double getMin() {
	return min;
}
public void setMin(double min) {
	this.min = min;
}
public double getMax() {
	return max;
}
public void setMax(double max) {
	this.max = max;
}
public double getStdDev() {
	return stdDev;
}
public void setStdDev(double stdDev) {
	this.stdDev = stdDev;
}
public double[] getArray() {
	return array;
}
}