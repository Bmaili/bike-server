import java.io.*;
import java.util.Scanner;
import java.net.Socket;
import java.net.UnknownHostException;

public class Client {

    public static void main(String[] args) {
        try {
            String send_mess, get_mess;
            Socket s = new Socket("", 8887);
            //Socket s = new Socket("39.103.183.238", 8887);

            InputStream is = s.getInputStream();// 套接字的输入流
            OutputStream os = s.getOutputStream();// 套接字的输出流
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(os, "UTF-8"));// 写入发送到服务器的消息
            BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"));// 读取服务器返回的消息
            Scanner scan = new Scanner(System.in);

            while (true) {

                System.out.println("请输入需要发送的指令：");
                send_mess = scan.next();// 从键盘接收数据并向服务器端发送
                bw.write(send_mess);
                bw.flush();

                get_mess = br.readLine();
                System.out.println("服务器回应：\n" + get_mess + "\n");
            }

        } catch (UnknownHostException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

}
