
int OnInit()
  {
//--- create timer
   EventSetTimer(1);
   
//---
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
//--- destroy timer
   EventKillTimer();
   
  }


void OnTimer()
{
      
      string to_split = send();
      if(StringLen(to_split) == 0) return;
      //Print(to_split);
      string sep=",";                // 分隔符为字符 
      ushort u_sep;                  // 分隔符字符代码 
      string result[];               // 获得字符串数组 
      u_sep=StringGetCharacter(sep,0); 
      int k=StringSplit(to_split,u_sep,result); 
      string name = result[0];
      double ask = StringToDouble(result[11]);
      double bid = StringToDouble(result[21]);
      int volume = StringToDouble(result[9]);
      //Print(ask,"  bid: ",bid," vol: ",volume);
      datetime Start_date = D'2018.11.26';
      ulong Start = ulong(Start_date)*1000;
      MqlTick last_tick; 
      MqlTick ticks[1];
 
      last_tick.ask=ask;
      last_tick.bid=bid;
      last_tick.time=TimeCurrent();
      last_tick.time_msc=TimeCurrent()*1000;
      last_tick.volume=volume;
      //SymbolInfoTick("EURUSD",last_tick);
      ////static int i = 0;
      ////ArrayResize(ticks,i+1);
      Print(" volume: ",volume/10000," ask : ",ask," bid: ",bid);
      ticks[0] = last_tick;
      CustomTicksAdd(_Symbol,ticks);
      //int copied = CopyTicks( Symbol() , Ticks, COPY_TICKS_ALL , Start, LONG_MAX);
      //Tick2Rates(Ticks,copied);
      //Print(copied);
}

  
void OnTick()
{

}

string send()
{
   string url = "http://hq.sinajs.cn/?list=sz002226";//江南化工
   string cookie=NULL,headers; 
   char   post[],result[]; 
   ResetLastError(); 
   
   //string str="name=jyq&age=30";
   //string str1="usdjpy:0.4,xauusd:0.4,usdcad:0.2";
   //StringToCharArray(data,post);
   string str;
   int res=WebRequest("POST",url,NULL,500,post,result,headers); 
   if(res==-1) 
     { 
      Print("Error in WebRequest. Error code  =",GetLastError()); 
      MessageBox("Add the address '"+url+"' to the list of allowed URLs on tab 'Expert Advisors'","Error",MB_ICONINFORMATION); 
     } 
   else 
     { 
      if(res==200) 
        { 
            str = CharArrayToString(result,0,WHOLE_ARRAY,CP_ACP);
            //Print(str);
        } 
      else 
         PrintFormat("Downloading '%s' failed, error code %d",url,res); 
     } 
     return str;
}