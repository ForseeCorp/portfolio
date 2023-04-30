package project1;
import java.util.*;     
public class AnalyticsUse
{
    static double[][] dataPoints = null;                    //2 dim array to hold all the data points

    public static void main(String[ ] args) throws Exception
    {
      String input_file = "dataset1.csv";
//        String input_file = "/home/s/sultans/web/java/demo/8inpout/analytics/dataset1.csv";
    
        if (args.length > 0)                                //if argument is provided 
            input_file = args[0];                           //use it as an input file

        readFile(input_file);                               //read the file into a 2 dim array
//      display(dataPoints);                                //print the 2 dim array
        compute(dataPoints);                                //compute and print

        System.out.print("\nTRANSPOSED");
        double[][] x = Analytics.transpose(dataPoints);     //transpose the 2 dim array 
        display(x);                                         //print transposed 2 dim array
    }

//--------------------------------------------------------------------------------
// Read the input file, cleanse it, and store into a 2 dimensional array
//--------------------------------------------------------------------------------
    static void readFile(String filename)
    { 
        int nRows = 0;                                  //number of lines/rows in file
        int nCols = 0;                                  //number of columns for each line
        String[] data = null;                           //1 dim array to hold string data for each line

        System.out.println("SOURCE INPUT...");
        try 
        {
            File    f1   = new File(filename);                                  //create a file object               
            Scanner file = new Scanner(f1);                                     //scanner for the input file

            LineNumberReader lnr = new LineNumberReader(new FileReader(f1));    //code to get the number of lines
            lnr.skip(Long.MAX_VALUE);                                           //skip to end
//          nRows = lnr.getLineNumber() +1;                                     //obtain the num of lines/rows      
            nRows = lnr.getLineNumber();                                        //for CSV there is an extra blank line      
            lnr.close();                                                        //close the object                                      

            dataPoints = new double[nRows][];                //create a 2 dim array with as many rows as lines in file 

            int row=0;
            int col=0;

            while (file.hasNextLine())                      //while there are lines in the file
            {
                String line = file.nextLine();              //get next line
                System.out.println(line);
                data            = line.split(",");          //split it on ,
                nCols           = data.length;              //get number of columns
                double[] cols   = new double[nCols];        //create a 1 dim array with as many cols as the line 
                dataPoints[row] = cols;                     //append the 1 dim array into the 2 dim array

                for (col=0; col < nCols; col++)             //loop for all columns
                {
                    try
                    {
                        double num = Double.parseDouble(data[col]);     //convert from String to double 
                        dataPoints[row][col] = num;                     //populate the 2 dim table              
                    } 
                    catch(Exception e)                                  //if error in conversion
                    {
//                      System.out.print  ("row:" + (row+1) + ", col:" + (col+1));                      //display error
//                      System.out.println(", value not numeric: " + data[col] + ", assuming null");    //display error

                        dataPoints[row][col] = Double.MIN_VALUE;         //assume bad/no data - place smallest double value 
                    }   
                }
                row++;                                                  //next row
            }
        }            
        catch (Exception e)
        {
            System.out.println(e);
        }
    }
//--------------------------------------------------------------------------------
// Display the 2 dimensional data array
//--------------------------------------------------------------------------------
    static void display(double[][] dataPoints)
    {
        System.out.println("\nDATA NORMALIZED...");

        for (double[] row : dataPoints)                  //loop through all rows of 2 dim array
        {
            for (double col : row)                       //loop through all the columns
                if (col == Double.MIN_VALUE)             //if smallest double value (assume bad/no data)
                    System.out.print("\t");              //bypass
                else
                    System.out.printf("%7.2f ", col);    //print the column value

            System.out.print("\n");
        }
    }
                
//--------------------------------------------------------------------------------
// Compute and print
//--------------------------------------------------------------------------------
    static void compute(double[] array)
    {
        System.out.println("\nCOMPUTATION...");

        for (double[] row : dataPoints)                 //loop through all rows                 
        {           
            System.out.print("\t");

            for (double col : row)                      //loop through all the columns
                if (col == Double.MIN_VALUE)            //if smallest double value (assume bad/no data)
                    System.out.print("\t");             //bypass
                else
                    System.out.printf("%7.2f ", col);   //print the column value
            
        //Perform row oriented analytics ------------------ 
           
            
            
            Analytics rowSum = new Analytics(array);
            rowSum.getSum();
            Analytics rowMedian = new Analytics(array);
            rowMedian.getMedian();
            Analytics rowAvg  = new  Analytics(array);
            rowAvg.getAverage();
            Analytics rowMin = new Analytics(array);
            rowMin.getMin();
            Analytics rowMax = new Analytics(array);
            rowMax.getMax();
            Analytics rowCount = new Analytics(array);
            rowCount.getCount();
            Analytics rowStdDev = new Analytics(array);
            rowStdDev.getStdDev();
        
            
            		
            
          //  double rowSum    = Analytics.sum(array);
          //  double rowAvg    = rowSum/rowCount;
          //  double rowMedian = Analytics.median(array);
          //  double rowMin    = Analytics.min(array);
          //  double rowMax    = Analytics.max(array);
          //  double rowStdDev = Analytics.stdDev(array);
            
            System.out.print (" | Count="    + rowCount);       //print row count
            System.out.printf("\tSum=%.2f"   , rowSum);         //print row sum   
            System.out.printf("\tAvg=%.2f"   , rowAvg);         //print row average
            System.out.printf("\tMedian=%.2f", rowMedian);      //print row median
            System.out.printf("\tMin=%.2f"   , rowMin);         //print row minimum value
            System.out.printf("\tMax=%.2f"   , rowMax);         //print row maximum value
            System.out.printf("\tstdDev=%.2f", rowStdDev);      //print row standard deviation
            System.out.println();       
        }                          

        System.out.println("\t --------------------------------------------------------------------------------");

        //Perform column oriented analytics --------------- 

        int maxCols = 0;                        //determine maximum number of columns
        for (double[] row : dataPoints)         //loop through all rows                 
            if (row.length > maxCols)           //if number of columns for the row > max
                maxCols = row.length;           //take it

        System.out.print("COUNT..:");            
        for (int col=0; col < maxCols; col++)                           //loop through all columns                  
        {           
            double[] colArray = Analytics.slice(dataPoints,"col",col);  //slice the array vertically
            double[] array    = Analytics.normalize(colArray);          //clean up the array  
            int colCount      = Analytics.count(array);                 //count the elements
            System.out.print("   " + colCount + "\t");                  //print column count
        }
        System.out.print("\nSUM....:");            
        for (int col=0; col < maxCols; col++)                           //loop through all columns                  
        {           
            double[] colArray = Analytics.slice(dataPoints,"col",col);  //slice the array vertically
            double[] array    = Analytics.normalize(colArray);          //clean up the array  
            double colSum     = Analytics.sum(array);                   //sum the elements
            System.out.printf("%7.2f ", colSum);                        //print column sum
        }
        System.out.print("\nAVERAGE:");            
        for (int col=0; col < maxCols; col++)                           //loop through all columns                  
        {           
            double[] colArray = Analytics.slice(dataPoints,"col",col);  //slice the array vertically
            double[] array    = Analytics.normalize(colArray);          //clean up the array  
            double colAvg     = Analytics.avg(array);                   //average the elements
            System.out.printf("%7.2f ", colAvg);                        //print column average
        }
        System.out.print("\nMEDIAN.:");            
        for (int col=0; col < maxCols; col++)                           //loop through all columns                  
        {           
            double[] colArray = Analytics.slice(dataPoints,"col",col);  //slice the array vertically
            double[] array    = Analytics.normalize(colArray);          //clean up the array  
            double colMedian  = Analytics.median(array);                //obtain the median
            System.out.printf("%7.2f ", colMedian);                     //print column median value
        }
        System.out.print("\nMIN....:");            
        for (int col=0; col < maxCols; col++)                           //loop through all columns                  
        {           
            double[] colArray = Analytics.slice(dataPoints,"col",col);  //slice the array vertically
            double[] array    = Analytics.normalize(colArray);          //clean up the array  
            double colMin     = Analytics.min(array);                   //obtain the minimum
            System.out.printf("%7.2f ", colMin);                        //print column minimum value
        }
        System.out.print("\nMAX....:");            
        for (int col=0; col < maxCols; col++)                           //loop through all columns                  
        {           
            double[] colArray = Analytics.slice(dataPoints,"col",col);  //slice the array vertically
            double[] array    = Analytics.normalize(colArray);          //clean up the array  
            double colMax     = Analytics.max(array);                   //obtain the maximum
            System.out.printf("%7.2f ", colMax);                        //print column maximum value
        }
        System.out.print("\nSTD-DEV:");            
        for (int col=0; col < maxCols; col++)                           //loop through all columns                  
        {           
            double[] colArray = Analytics.slice(dataPoints,"col",col);  //slice the array vertically
            double[] array    = Analytics.normalize(colArray);          //clean up the array  
            double colStdDev  = Analytics.stdDev(array);                //obtain the standard deviation
            System.out.printf("%7.2f ", colStdDev);                     //print column standard deviation
        }


        //Perform final analytics (entire dataset)------------------ 

        System.out.println("\n\n--------OVERALL-------------");
        double[] allArray = Analytics.slice(dataPoints,"all",0);        //convert 2dim array to 1dim
        double[] array    = Analytics.normalize(allArray);              //clean up the array  
        System.out.println(Analytics.toString(array));                  //call the static toString() method 


        //Print Analytics for Column 1---------------------------- 

        System.out.println("\n--------COLUMN 1-------------");
        double[] colArray = Analytics.slice(dataPoints,"col",0);        //slice the array vertically
        double[] array1   = Analytics.normalize(colArray);              //clean up the array  
        System.out.println(Analytics.toString(array1));                 //call the static toString() method 
    }
}
