#include "U8glib.h"  //加载显示库文件

String comdata = "";
String comdata1 = "";
String comdata2 = "";
int commaPosition; 

U8GLIB_SH1106_128X64 u8g(U8G_I2C_OPT_NONE);  // I2C / TWI 实例化

void setup() {
  Serial.begin(9600);
  Serial.println("connected");
}


void loop() {
  while (Serial.available() > 0)  
    {
        comdata += char(Serial.read());
        delay(2);
    }
    if (comdata.length() > 0)
    {
        //Serial.println(comdata);
        commaPosition = comdata.indexOf('/');
        if(commaPosition != -1)
          {
          comdata1 = (comdata.substring(0,commaPosition));
          //Serial.println(comdata1);
          comdata2 = comdata.substring(commaPosition+1, comdata.length());
          commaPosition = comdata2.indexOf('/');
          if(commaPosition != -1)
            {
              comdata2 = (comdata2.substring(0,commaPosition));
              }
          comdata = "";
          show();
          }
  }
}

void show(){
  u8g.firstPage();  //一下是显示实现部分
  do {
  u8g.setFont(u8g_font_fub14);//设置字体和自号，目前测试字号有fub14,17,20,30
  u8g.setPrintPos(0, 20); //显示的位置
  u8g.print(comdata1);//显示变量i的值
  u8g.setFont(u8g_font_fub14);//设置字体和自号，目前测试字号有fub14,17,20,30
  u8g.setPrintPos(0, 50); //显示的位置
  u8g.print(comdata2);//显示变量i的值
  } while( u8g.nextPage() );
  delay(100);//显示的时间间隔
}
