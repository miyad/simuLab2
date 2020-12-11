import java.util.Scanner;
public class CompilerAssignment {
    public static void main(String[] args) {
        Scanner sc= new Scanner(System.in);String str;int len;boolean exit=false;
        while (!exit){System.out.print("Choose an option:\n1.Validate CSE ID\n2.Validate CSE or EEE mail\n3.Validate a Password\n4.Validate a Number\n5.Validate a Pattern\n6.Exit\n");
            String check=sc.nextLine();
            switch (Integer.parseInt(check)){
                case 1:
                    System.out.print("Enter a CSE ID: ");
                    str= sc.nextLine();
                    if(str.length()==9){
                        if(Integer.parseInt(str.substring(0,3))==11 ){
                            if(Integer.parseInt(str.substring(3,5))>=5 && Integer.parseInt(str.substring(3,5))<=20 ){
                                if(Integer.parseInt(str.substring(5,6))>=1 && Integer.parseInt(str.substring(5,6))<=3){
                                    if(Integer.parseInt(str.substring(6,9))>=1 && Integer.parseInt(str.substring(6,9))<=999){
                                        System.out.print("Valid\n");}
                                    else System.out.print("Not Valid\n");
                                }
                                else System.out.print("Not Valid\n");
                            }
                            else System.out.print("Not Valid\n");
                        }
                        else System.out.print("Not Valid\n");
                    }
                    else System.out.print("Not Valid\n");
                    break;
                case 2:
                    System.out.print("Enter a CSE or EEE mail: ");
                    str= sc.nextLine();len= str.length()-16;
                    try{
                        if (str.substring(len,str.length()).equals("@bscse.uiu.ac.bd") ||str.substring(len,str.length()).equals("@bseee.uiu.ac.bd") ) {
                            if (Integer.parseInt(str.substring(len - 3, len)) >= 1 && Integer.parseInt(str.substring(len - 3, len)) <= 999) {
                                if (Integer.parseInt(str.substring(len - 4, len - 3)) >= 1 && Integer.parseInt(str.substring(len - 4, len - 3)) <= 3) {
                                    if (Integer.parseInt(str.substring(len - 6, len - 4)) >= 5 && Integer.parseInt(str.substring(len - 6, len - 4)) <= 18)
                                        System.out.print("Valid\n");
                                }
                            }
                        }
                        else System.out.print("Not Valid\n");
                    }
                    catch(NumberFormatException e){
                        System.out.print("Not Valid\n");
                    }
                    catch(IndexOutOfBoundsException e){
                        System.out.print("Not Valid\n");
                    }
                    break;
                case 6:
                    exit=true;
            }
        }
    }
}
