# ColoredPrinter GuideLine
ColoredPrinter is an easy-use tool, which has packaged verious color constants and font styles to make the output more colorful in your python program.

 + Enivorment  
    ~ python 3.7.5
 
 + How to get it？
    Just run the command  ```pip install colouredprinter -i https://pypi.org/simple ```
 
 + UseAge
   
   - import the module  
      ``` from colouredprinter.printer.ColouredPrinter Printer ```  
      ``` from colouredprinter.style.FontStyleConstant import FontStyle, BackgroundColor```  
      ``` from colouredprinter.color.ColorConstant import FrontColor ```  
   - init the Printer  
     ``` printer = Printer() ```  
   - set the fontstyle  
     ``` printer.setFontStyle(FontStyle.UNDERLINE) ```  
   - set the front-color  
     ``` printer.setFrontColor(FrontColor.DARKORCHILD) ```
   - set the background-color  
     ``` printer.setBackGroundColor(BackgroundColor.YELLOW) ```  
   - invoke the ```println``` function  
     ``` printer.println('Now,you can see the cyan output with underline and yellow background!') ```    
     then ,you will get the ouput as it describles.       
   - To Reset The OutPut Style To Defult  
     ```printer.reset()``` 
+ The Difference Between ```printer.print()``` and ```printer.println()```  

   - If you have  programing experiences on java,you may have known it.  
   the ```printer.print()``` function dose not  end with a newline,but the ```printer.println()``` will do it.  

+ Color Constant          

     |   ColorName  | 
     | -------------|
     |    BLACK     |    
     |     RED      |
     |   GREEN      |
     |   YELLOW     |
     |   BLUE       |
     | DARKORCHILD  |
     |   CYAN       |
     |   WHITE      |  

+  Font Styles  

     |       StyleName     |  
     | --------------------|
     |   HIGHLIGHT         |    
     |    NO_BOLD          |
     |   UNDERLINE         |
     |   NO_UNDERLINE      |
     |    SPARKLE          |
     |   NO_SPARKLE        |
     |  REVERSE_DISPLAY    |
     | NO_REVERSE_DISPLAY  |            
+  Something Confusing
   - The FontStyles make no difference on windows's terminal,but work on IDE such as Pycharm.
   
