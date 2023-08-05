![](https://owl.cmoney.com.tw/Owl/resources/images/logo.png)

---

# OwlData 數據貓頭鷹 API

數據貓頭鷹官方網站: https://owl.cmoney.com.tw/Owl/

--------

## Outline

- [OwlData 數據貓頭鷹 API](#owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api)
  - [Outline](#outline)
  - [Dependencies](#dependencies)
  - [Install](#install)
  - [HTTP Authentication](#http-authentication)
    - [Flow Control](#flow-control)
    - [Code Example](#code-example)
  - [Quick Start](#quick-start)
  - [Data Function](#data-function)
  - [Notes](#notes)
  - [Contribute](#contribute)
  
## Dependencies

- pandas
- requests

## Install

安裝資源可以詳見 Github at https://github.com/owldb168/owldata

By PyPI

``` python
pip install owldata
```

Install source from GitHub

``` sh
git clone https://github.com/owldb168/owldata.git
cd owldata
python setup.py install
```

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

## HTTP Authentication

&nbsp;&nbsp;&nbsp;&nbsp;介接端須先透過取得的應用程式編號與應用程式密鑰取得一次性的有效交易驗證碼，於每次API呼叫時帶入 HTTP HEADER 提供驗證才能使用相關API。此驗證碼於特定時間後會 timeout過期，此時必須重新取得交易驗證碼得以再次操作相關API。

### Flow Control

![情境流程示意](https://owl.cmoney.com.tw/Owl/resources/images/img_api_01.png)

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

### Code Example

使用 OwlData 模組輸入 AppID 與應用程式密鑰進行登入，並呼叫欲查詢資料表

``` python
import owldata

# 輸入數據貓頭鷹會員 AppID & 應用程式密鑰
appid = '請輸入 AppID'
appsecret = '請輸入 應用程式密鑰'

# 引用函數取得資料
owlapp = owldata.OwlData(appid, appsecret)
```

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

## Quick Start

快速拿取個股歷史資料

``` python
import owldata

# 輸入數據貓頭鷹會員 AppID & 應用程式密鑰
appid = '請輸入 AppID'
appsecret = '請輸入 應用程式密鑰'

# 引用函數取得資料
owlapp = owldata.OwlData(appid, appsecret)

# 擷取台積電股價 from 2019/08/12 to 2019/08/13
stock_price = owlapp.ssp("2330", "20190812", "20190813")
stock_price.head()
```

## Data Function

OwlData 使用方法，使用 OwlData 不同方法擷取所需要的資料，並可以利用參數 colist 進行欄位篩選

1. 個股日收盤行情 (Single Stock Price, SSP)

    <br>依指定日期區間，撈取指定股票代號的股價資訊
    <br>

   ``` python
   OwlData.ssp(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
   ```

    <table>
    <tr>
        <td rowspan="4"><b>Parameters<b></td>
        <td> - <b> sid </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;股票代號
        </td>
    </tr>
    <tr>
        <td> - <b>  bpd </b> : <i> string </i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;設定查詢起始日期 8 碼數字，格式: yyyymmdd
        </td>
    </tr>
    <tr>
        <td> - <b> epd</b> : <i> string</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;設定查詢結束日期 8 碼數字，格式: yyyymmdd
        </td>
    </tr>
    <tr>
        <td> - <b> colist</b> : <i> list, default None</i>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
        </td>
    </tr>
    <tr>
        <td><b> Returns</b></td><td>DataFrame or Series</td>
    </tr>
    <tr>
        <td colspan="2">
        <b> Note</b>
        <br>
            &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
        </td>
    </tr>
    </table>

   - 欄位

    <table>
        <tr>
            <th colspan="4">免費版</th>
        </tr>
        <tr>
            <td>日期</td>
            <td>股票名稱</td>
            <td>開盤價</td>
            <td>最高價</td>
        </tr>
        <tr>
            <td>最低價</td>
            <td>收盤價</td>
            <td>成交量</td>
            <td></td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="5">付費版</th>
        </tr>
        <tr>
            <td>日期</td>
            <td>股票名稱</td>
            <td>開盤價</td>
            <td>最高價</td>
            <td>最低價</td>
        </tr>
        <tr>
            <td>收盤價</td>
            <td>成交量</td>
            <td>漲跌</td>
            <td>漲幅(%)</td>
            <td>振幅(%)</td>
        </tr>
        <tr>
            <td>成交筆數</td>
            <td>成交金額(千)</td>
            <td>均張</td>
            <td>均價</td>
            <td>股本(百萬)</td>
        </tr>
        <tr>
            <td>總市值(億)</td>
            <td>本益比</td>
            <td>股價淨值比</td>
            <td>本益比(近四季)</td>
            <td></td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台積電股價 from 2019/08/12 to 2019/08/13
    >>> colist = ['日期', '股票名稱', '開盤價', '最高價', '最低價' , '收盤價','成交量']
    >>> owlapp.ssp("2330", "20190812", "20190813", colist)
    [out]

           日期      股票名稱    開盤價    最高價    最低價     收盤價   成交量
    0   2019-08-12    台積電    254.50   254.50    251.00    251.00    24732
    1   2019-08-13    台積電    249.00   249.50    246.50    246.50    25045
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

2. 多股每日收盤行情 (Multi-Stock Price, MSP)

    <br>依指定日期，撈取全上市櫃台股的股價資訊
    <br>

    ``` python
    OwlData.msp(dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
            </td>
        </tr>
            <tr>
                <td> - <b> colist </b>: 
                <i> list, default None</i>
                <br>
                    &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
                </td>
            </tr>
            <tr>
                <td><b> Returns</b></td><td>DataFrame or Series</td>
            </tr>
            <tr>
                <td colspan="2">
                <b> Note</b>
                <br>
                    &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
                </td>
            </tr>
    </table>

     - 欄位

    <table>
        <tr>
            <th colspan="4">免費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>開盤價</td>
        </tr>
        <tr>
            <td>最高價</td>
            <td>最低價</td>
            <td>收盤價</td>
            <td>成交量</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="7">付費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>開盤價</td>
            <td>最高價</td>
            <td>最低價</td>
            <td>收盤價</td>
        </tr>
        <tr>
            <td>成交量</td>
            <td>漲跌</td>
            <td>漲幅(%)</td>
            <td>振幅(%)</td>
            <td>成交筆數</td>
            <td>成交金額(千)</td>
            <td>均張</td>
        </tr>
        <tr>
            <td>均價</td>
            <td>股本(百萬)</td>
            <td>總市值(億)</td>
            <td>本益比</td>
            <td>股價淨值比</td>
            <td>本益比(近四季)</td>
            <td></td>
        </tr>
    </table>

     - 範例

    ``` python
    # 擷取台股上市上櫃  2019/08/01 所有盤後資訊
    >>>colist = ['股票代號','股票名稱','日期','開盤價','最高價','最低價','收盤價','成交量']
    >>> owlapp.msp("20190801",colist)

    [out]
        股票代號  股票名稱     日期     開盤價   最高價   最低價   收盤價   成交量
    0     1101     台泥   2019-08-01   44.50   44.55    44.00   44.05    33643
    1     1102     亞泥   2019-08-01   41.45   41.70    41.20   41.40     8384
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

3. 個股財務簡表 (Financial Statements Single, FIS)

    <br>依據 di 決定查詢資料頻率，並依股票代號，撈取指定區間的財務報表資訊
    <br>y(年)、 q(季) 是撈取財務報表資訊；m(月) 是撈取營收相關資訊

    ```python
    OwlData.fis(sid:str, di:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="5"><b>Parameters<b></td>
            <td> - <b>  sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b> di </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定資料時間頻率
                <ul style="list-style-type:disc;">
                    <li>Y : 年度, 格式 : yyyy</li>
                    <li>Q : 季度, 格式 : yyyyqq</li>
                    <li>M : 月份, 格式 : yyyymm</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢起始日期
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢結束日期
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 季度日期格式 yyyqq, 其中 qq 請輸入 01 - 04, 分別表示為第一季至第四季
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 參數 di 大小寫無異
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
            <th colspan="5">免費版</th>
        </tr>
        <tr>
            <td colspan="5">年與季財報欄位</td>
        </tr>
        <tr>
            <td>年度</td>
            <td>年季</td>
            <td>流動資產(千)</td>
            <td>非流動資產(千)</td>
            <td>資產總計(千)</td>
        </tr>
        <tr>
            <td>流動負債(千)</td>
            <td>非流動負債(千)</td>
            <td>負債總計(千)</td>
            <td>權益總計(千)</td>
            <td>營業收入淨額(千)</td>
        </tr>
        <tr>
            <td>營業成本(千)</td>
            <td>營業毛利(千)</td>
            <td>營業費用(千)</td>
            <td>營業利益(千)</td>
            <td></td>
        </tr>
        <tr>
            <td colspan="5">月營收欄位</td>
        </tr>
        <tr>
            <td>年月</td>
            <td>單月合併營收(千)</td>
            <td>單月合併營收年成長(%)</td>
            <td>累計合併營收(千)</td>
            <td></td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="7">付費版</th>
        </tr>
        <tr>
            <td colspan="7">年與季財報欄位</td>
        </tr>
        <tr>
            <td>年度</td>
            <td>年季</td>
            <td>流動資產(千)</td>
            <td>現金及約當現金(千)</td>
            <td>短期投資合計(千)</td>
            <td>應收帳款淨額(千)</td>
            <td>存貨(千)</td>
        </tr>
        <tr>
            <td>非流動資產(千)</td>
            <td>不動產、廠房及設備(千)</td>
            <td>無形資產(千)</td>
            <td>資產總計(千)</td>
            <td>流動負債(千)</td>
            <td>短期借款(千)</td>
            <td>應付票據(千)</td>
        </tr>
        <tr>
            <td>應付帳款(千)</td>
            <td>非流動負債(千)</td>
            <td>應付公司債(千)</td>
            <td>負債總計(千)</td>
            <td>普通股股本(千)</td>
            <td>特別股股本(千)</td>
            <td>公告每股淨值(元)</td>
        </tr>
        <tr>
            <td>保留盈餘(千)</td>
            <td>資本公積(千)</td>
            <td>庫藏股票(千)</td>
            <td>母公司業主權益(千)</td>
            <td>權益總計(千)</td>
            <td>營業收入淨額(千)</td>
            <td>營業成本(千)</td>
        </tr>
        <tr>
            <td>營業毛利(千)</td>
            <td>營業費用(千)</td>
            <td>營業利益(千)</td>
            <td>營業外收入及支出(千)</td>
            <td>稅前純益(千)</td>
            <td>所得稅(千)</td>
            <td>繼續營業單位損益(千)</td>
        </tr>
        <tr>
            <td>稅後純益(千)</td>
            <td>公告基本每股盈餘(元)</td>
            <td>營業活動現金流量(千)</td>
            <td>投資活動現金流量(千)</td>
            <td>籌資活動現金流量(千)</td>
            <td>自由現金流量(千)</td>
            <td>槓桿比率(%)</td>
        </tr>
        <tr>
            <td>流動比率(%)</td>
            <td>速動比率(%)</td>
            <td>負債比率(%)</td>
            <td>淨值成長率(%)</td>
            <td>應付帳款週轉率(次)</td>
            <td>應收帳款週轉率(次)</td>
            <td>存貨週轉率(次)</td>
        </tr>
        <tr>
            <td>固定資產週轉率(次)</td>
            <td>總資產週轉率(次)</td>
            <td>淨值週轉率(次)</td>
            <td>毛利率(%)</td>
            <td>營業費用率(%)</td>
            <td>營業利益率(%)</td>
            <td>稅前純益率(%)</td>
        </tr>
        <tr>
            <td>稅後純益率(%)</td>
            <td>稅前權益報酬率(%)</td>
            <td>稅後權益報酬率(%)</td>
            <td>稅前資產報酬率(%)</td>
            <td>稅後資產報酬率(%)</td>
            <td>利息保障倍數(倍)</td>
            <td>營收成長率(%)</td>
        </tr>
        <tr>
            <td>總資產成長率(%)</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td colspan="7">月營收欄位</td>
        </tr>
        <tr>
            <td>年月</td>
            <td>單月合併營收(千)</td>
            <td>去年單月合併營收(千)</td>
            <td>單月合併營收年成長(%)</td>
            <td>單月合併營收月變動(%)</td>
            <td>累計合併營收(千)</td>
            <td>去年累計合併營收(千)</td>
        </tr>
        <tr>
            <td>累計合併營收成長(%)</td>
            <td>近三月合併營收(千)</td>
            <td>近三月合併營收年成長(%)</td>
            <td>近三月合併營收月變動(%)</td>
            <td>近12月合併營收(千)</td>
            <td>近12月合併營收成長(%)</td>
            <td></td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台積電財務簡表 from 2016 to 2017
    >>> colist = ['年度', '流動資產(千)', '非流動資產(千)', '資產總計(千)', '流動負債(千)', '非流動負債(千)', '負債總計(千)']
    >>> owlapp.fis('y', "2330", "2017", "2018", colist)

    [out]
            年度     流動資產(千)   非流動資產(千)   資產總計(千)   流動負債(千)    非流動負債(千)    負債總計(千)
    0   2017-12-31    92719914      179837135      272557049      65192960        54716873        119909833
    1   2018-12-31   110380695      233704423      344085118      64503844        82201818        146705662

    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

4. 多股財務簡表 (Financial Statements Multi, FIM)

    <br>依據 di 決定查詢資料頻率，並依指定區間，撈取全上市櫃台股的財務報表資訊
    <br> y(年)、 q(季) 是撈取財務報表資訊；m(月) 是撈取營收相關資訊

    ``` python
    OwlData.fim(di:str, dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="3"><b>Parameters<b></td>
            <td> - <b> di </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定資料時間頻率
                <ul style="list-style-type:disc;">
                    <li>Y : 年度, 格式 : yyyy</li>
                    <li>Q : 季度, 格式 : yyyyqq</li>
                    <li>M : 月份, 格式 : yyyymm</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td> - <b>  dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 季度日期格式 yyyqq, 其中 qq 請輸入 01 - 04, 分別表示為第一季至第四季
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 參數 di 大小寫無異
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
            <th colspan="4">免費</th>
        </tr>
        <tr>
            <td colspan="4">年與季財報欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>年季</td>
        </tr>
        <tr>
            <td>流動資產(千)</td>
            <td>非流動資產(千)</td>
            <td>資產總計(千)</td>
            <td>流動負債(千)</td>
        </tr>
        <tr>
            <td>非流動負債(千)</td>
            <td>負債總計(千)</td>
            <td>權益總計(千)</td>
            <td>營業收入淨額(千)</td>
        </tr>
        <tr>
            <td>營業成本(千)</td>
            <td>營業毛利(千)</td>
            <td>營業費用(千)</td>
            <td>營業利益(千)</td>
        </tr>
        <tr>
            <td colspan="4">月營收欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年月</td>
            <td>單月合併營收(千)</td>
        <tr>
        </tr>
            <td>單月合併營收年成長(%)</td>
            <td>累計合併營收(千)</td>
            <td></td>
            <td></td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="8">付費版</th>
        </tr>
        <tr>
            <td colspan="8">年與季財報欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>年季</td>
            <td>存貨(千)</td>
            <td>非流動資產(千)</td>
            <td>不動產、廠房及設備(千)</td>
            <td>無形資產(千)</td>
        </tr>
        <tr>
            <td>資產總計(千)</td>
            <td>流動負債(千)</td>
            <td>短期借款(千)</td>
            <td>應付票據(千)</td>
            <td>應付帳款(千)</td>
            <td>非流動負債(千)</td>
            <td>應付公司債(千)</td>
            <td>負債總計(千)</td>
        </tr>
        <tr>
            <td>普通股股本(千)</td>
            <td>特別股股本(千)</td>
            <td>公告每股淨值(元)</td>
            <td>保留盈餘(千)</td>
            <td>資本公積(千)</td>
            <td>庫藏股票(千)</td>
            <td>母公司業主權益(千)</td>
            <td>權益總計(千)</td>
        </tr>
        <tr>
            <td>營業收入淨額(千)</td>
            <td>營業成本(千)</td>
            <td>營業毛利(千)</td>
            <td>營業費用(千)</td>
            <td>營業利益(千)</td>
            <td>營業外收入及支出(千)</td>
            <td>稅前純益(千)</td>
            <td>所得稅(千)</td>
        </tr>
        <tr>
            <td>繼續營業單位損益(千)</td>
            <td>稅後純益(千)</td>
            <td>公告基本每股盈餘(元)</td>
            <td>營業活動現金流量(千)</td>
            <td>投資活動現金流量(千)</td>
            <td>籌資活動現金流量(千)</td>
            <td>自由現金流量(千)</td>
            <td>槓桿比率(%)</td>
        </tr>
        <tr>
            <td>流動比率(%)</td>
            <td>速動比率(%)</td>
            <td>負債比率(%)</td>
            <td>淨值成長率(%)</td>
            <td>應付帳款週轉率(次)</td>
            <td>應收帳款週轉率(次)</td>
            <td>存貨週轉率(次)</td>
            <td>固定資產週轉率(次)</td>
        </tr>
        <tr>
            <td>總資產週轉率(次)</td>
            <td>淨值週轉率(次)</td>
            <td>毛利率(%)</td>
            <td>營業費用率(%)</td>
            <td>營業利益率(%)</td>
            <td>稅前純益率(%)</td>
            <td>稅後純益率(%)</td>
            <td>稅前權益報酬率(%)</td>
        </tr>
        <tr>
            <td>稅後權益報酬率(%)</td>
            <td>稅前資產報酬率(%)</td>
            <td>稅後資產報酬率(%)</td>
            <td>利息保障倍數(倍)</td>
            <td>營收成長率(%)</td>
            <td>總資產成長率(%)</td>
            <td></td>
            <td></td>
        </tr>
        <tr>
            <td colspan="8">月營收欄位</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年月</td>
            <td>單月合併營收(千)</td>
            <td>去年單月合併營收(千)</td>
            <td>單月合併營收年成長(%)</td>
            <td>單月合併營收月變動(%)</td>
            <td>累計合併營收(千)</td>
        </tr>
        <tr>
            <td>去年累計合併營收(千)</td>
            <td>累計合併營收成長(%)</td>
            <td>近三月合併營收(千)</td>
            <td>近三月合併營收年成長(%)</td>
            <td>近三月合併營收月變動(%)</td>
            <td>近12月合併營收(千)</td>
            <td>近12月合併營收成長(%)</td>
            <td></td>
        </tr>
    </table>

   - 範例

        ``` python
        # 台股上市上櫃財務簡表 from 2018
        >>> colist = ["股票代號","股票名稱","年度","流動資產(千)","非流動資產(千)","資產總計(千)","流動負債(千)"]
        >>> owlapp.fim('Y',"2018",colist)

        [out]
            股票代號  股票名稱      年度     流動資產(千)   非流動資產(千)   資產總計(千)   流動負債(千)
       0     1101     台泥    2018-12-31    110380695      233704423      344085118      64503844
       1     1102     亞泥    2018-12-31     80358506      198829492      279187998      62804294

        ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

5. 法人籌碼個股資料 (Corporate Chip Single, CHS)

    <br>依指定日期區間，撈取指定股票的三大法人買賣狀況和該股票的融資券狀況
    <br>

   ``` python
   OwlData.chs(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
   ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;設定查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
            <th colspan="5">免費版</th>
        </tr>
        <tr>
            <td>日期</td>
            <td>買賣超合計</td>
            <td>外資買賣超</td>
            <td>投信買賣超</td>
            <td>自營買賣超</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="5">付費版</th>
        </tr>
        <tr>
            <td>日期</td>
            <td>買賣超合計</td>
            <td>法人買賣超金額(千)</td>
            <td>法人持股比率(%)</td>
            <td>外資買賣超</td>
        </tr>
        <tr>
            <td>外資買賣超金額(千)</td>
            <td>外資持股比率(%)</td>
            <td>投信買賣超</td>
            <td>投信買賣超金額(千)</td>
            <td>投信庫存</td>
        </tr>
        <tr>
            <td>投信持股比率(%)</td>
            <td>自營買賣超</td>
            <td>自營買賣超金額(千)</td>
            <td>自營商買賣超(自行買賣)</td>
            <td>自營商買賣超(避險)</td>
        </tr>
        <tr>
            <td>自營商庫存</td>
            <td>自營商持股比率(%)</td>
            <td>資餘</td>
            <td>資增減</td>
            <td>券餘</td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台積電法人籌碼資料 from 2019/08/01 to 2019/08/02
    >>> colist = ['日期','買賣超合計','外資買賣超','投信買賣超','自營商買賣超']
    >>> owlapp.chs("2330", "20190801", "20190802",colist)

    [out]
            日期     買賣超合計   外資買賣超   投信買賣超  自營商買賣超
    0   2019-08-01    -9058       -10675        196        1421
    1   2019-08-02    -8712        -9356       -235         879
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

6. 法人籌碼多股資料 (Corporate Chip Multi, CHM)

    <br>查詢指定日期，全上市櫃台股的三大法人買賣狀況和融資券狀況
    <br>

   ```python
   OwlData.chm(dt:str,colist:list) -> DataFrame
   ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期 8碼，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
            <th colspan="7">免費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>買賣超合計</td>
        </tr>
        <tr>
            <td>外資買賣超</td>
            <td>投信買賣超</td>
            <td>自營買賣超</td>
            <td></td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="5">付費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>買賣超合計</td>
            <td>法人買賣超金額(千)</td>
        </tr>
        <tr>
            <td>法人持股比率(%)</td>
            <td>外資買賣超</td>
            <td>外資持股比率(%)</td>
            <td>投信買賣超</td>
            <td>投信買賣超金額(千)</td>
        </tr>
        <tr>
            <td>投信庫存</td>
            <td>投信持股比率(%)</td>
            <td>自營買賣超</td>
            <td>自營買賣超金額(千)</td>
            <td>自營商買賣超(自行買賣)</td>
        </tr>
        <tr>
            <td>自營商買賣超(避險)</td>
            <td>自營商庫存</td>
            <td>自營商持股比率(%)</td>
            <td>資餘</td>
            <td>資增減</td>
        </tr>
        <tr>
            <td>券餘</td>
            <td>券增減</td>
            <td>券資比</td>
            <td>資使用率</td>
            <td>券使用率</td>
        </tr>
        <tr>
            <td>當沖比率</td>
            <td></td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台股上市上櫃  from 2019/08/01 所有法人籌碼資訊
    >>> colist = ['股票代號','股票名稱','日期','買賣超合計','外資買賣超','投信買賣超','自營商買賣超']
    >>> owlapp.chm("20190916",colist)

    [out]
        股票代號 股票名稱      日期      買賣超合計  外資買賣超  投信買賣超  自營商買賣超
    0     1101    台泥     2019-09-16    -3470       -2323        0         -1147
    1     1102    亞泥     2019-09-16     2008        1712       50           246
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

7. 技術指標 個股 (Technical Indicators Single, TIS)

    <br>依指定日期區間，撈取指定股票的技術指標數值
    <br>

    ```python
    OwlData.tis(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束日期 8 碼數字，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
            <th colspan="6">免費版</th>
        </tr>
        <tr>
            <td>日期</td>
            <td>K(9)</td>
            <td>D(9)</td>
            <td>RSI(5)</td>
            <td>RSI(10)</td>
            <td>DIF-MACD</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="5">付費版</th>
        </tr>
        <tr>
            <td>日期</td>
            <td>K(9)</td>
            <td>D(9)</td>
            <td>RSI(5)</td>
            <td>RSI(10)</td>
        </tr>
        <tr>
            <td>DIF</td>
            <td>MACD</td>
            <td>DIF-MACD</td>
            <td>W%R(5)</td>
            <td>W%R(10)</td>
        </tr>
        <tr>
            <td>+DI(14)</td>
            <td>-DI(14)</td>
            <td>ADX(14)</td>
            <td>Alpha(250D)</td>
            <td>Beta係數(21D)</td>
        </tr>
        <tr>
            <td>Beta係數(65D)</td>
            <td>Beta係數(250D)</td>
            <td>年化波動度(21D)</td>
            <td>年化波動度(250D)</td>
            <td>乖離率(20日)</td>
        </tr>
        <tr>
            <td>乖離率(60日)</td>
            <td>乖離率(250日)</td>
            <td>EWMA波動率(%)</td>
            <td>+DM(14)</td>
            <td>-DM(14)</td>
        </tr>
    </table>

    - 範例

    ``` python
    # 擷取台積電技術指標 from 2019/08/01 to 2019/08/02
    >>> colist = ['日期', 'K(9)', 'D(9)', 'RSI(5)', 'RSI(10)',"DIF","MACD","DIF-MACD"]
    >>> owlapp.tis("2330", "20190801", "20190802", colist)

    [out]
            日期     K(9)    D(9)   RSI(5)   RSI(10)   DIF    MACD    DIF-MACD
    0   2019-08-01  39.80   60.45   30.51    51.65    5.12    5.73     -0.61
    1   2019-08-02  28.62   49.84   17.88    40.98    4.21    5.43     -1.22
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

8. 技術指標 多股 (Technical Indicators Multi, TIM)

    <br>查詢指定日期，全上市櫃台股的技術指標數值
    <br>

    ```python
    OwlData.tim(dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一日期 8碼，格式: yyyymmdd
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

     - 欄位

    <table>
        <tr>
            <th colspan="5">免費</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>K(9)</td>
            <td>D(9)</td>
        </tr>
        <tr>
            <td>RSI(5)</td>
            <td>RSI(10)</td>
            <td>DIF</td>
            <td>MACD</td>
            <td>DIF-MACD</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="5">付費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>日期</td>
            <td>K(9)</td>
            <td>D(9)</td>
        </tr>
        <tr>
            <td>RSI(5)</td>
            <td>RSI(10)</td>
            <td>DIF</td>
            <td>MACD</td>
            <td>DIF-MACD</td>
        </tr>
        <tr>
            <td>W%R(5)</td>
            <td>W%R(10)</td>
            <td>+DI(14)</td>
            <td>-DI(14)</td>
            <td>ADX(14)</td>
        </tr>
        <tr>
            <td>Alpha(250D)</td>
            <td>Beta係數(21D)</td>
            <td>Beta係數(65D)</td>
            <td>Beta係數(250D)</td>
            <td>年化波動度(21D)</td>
        </tr>
        <tr>
            <td>年化波動度(250D)</td>
            <td>乖離率(20日)</td>
            <td>乖離率(60日)</td>
            <td>乖離率(250日)</td>
            <td>EWMA波動率(%)</td>
        </tr>
        <tr>
            <td>+DM(14)</td>
            <td>-DM(14)</td>
            <td></td>
            <td></td>
            <td></td>
        </tr>
    </table>

     - 範例

    ``` python
    # 擷取台股上市上櫃  from 2019/08/01 所有技術指標資訊
    >>> colist = ['股票代號', '股票名稱', '日期', 'K(9)', 'D(9)', 'RSI(5)',
            'RSI(10)',"DIF","MACD","DIF-MACD"]
    >>> owlapp.tim("20190801", colist)

    [out]
        股票代號 股票名稱     日期        K(9)    D(9)   RSI(5)  RSI(10)    DIF    MACD   DIF-MACD
    0     1101   台泥     2019-08-02   27.82   42.49    18.10    29.52   -0.13   -0.01    -0.13
    1     1102   亞泥     2019-08-02    9.00   11.74    11.85    25.02   -0.62   -0.31    -0.31
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

9. 公司基本資料 多股 (Company Information Multi, CIM)

    <br>撈取上市櫃台股的公司基本資料
    <br>

    ``` python
    OwlData.cim(colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="1"><b>Parameters<b></td>
            <td> - <b> colist </b> : <i> list, default None </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

   - 欄位

    <table>
        <tr>
            <th colspan="5">免費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>中文簡稱</td>
            <td>公司名稱</td>
            <td>地址</td>
        </tr>
        <tr>
            <td>電話</td>
            <td>上市上櫃</td>
            <td>成立日期</td>
            <td>產業名稱</td>
            <td>董事長</td>
        </tr>
        <tr>
            <td>總經理</td>
            <td>發言人</td>
            <td>發言人職稱</td>
            <td>經營項目</td>
            <td>交易所公告股本(千)</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="5">付費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>中文簡稱</td>
            <td>公司名稱</td>
            <td>地址</td>
        </tr>
        <tr>
            <td>電話</td>
            <td>上市上櫃</td>
            <td>存續年度</td>
            <td>成立日期</td>
            <td>上市日期</td>
        </tr>
        <tr>
            <td>上櫃日期</td>
            <td>興櫃日期</td>
            <td>公發日期</td>
            <td>董事長</td>
            <td>總經理</td>
        </tr>
        <tr>
            <td>發言人</td>
            <td>發言人職稱</td>
            <td>產業代號</td>
            <td>產業名稱</td>
            <td>產業指數代號</td>
        </tr>
        <tr>
            <td>產業指數名稱</td>
            <td>股票過戶機構</td>
            <td>經營項目</td>
            <td>前年度內銷比重(%)</td>
            <td>前年度外銷比重(%)</td>
        </tr>
        <tr>
            <td>交易所普通股股本(千)</td>
            <td>交易所特別股股本(千)</td>
            <td>交易所普通股股數(千)</td>
            <td>交易所特別股股數(千)</td>
            <td>交易所公告股本(千)</td>
        </tr>
        <tr>
            <td>實收資本額(百萬)</td>
            <td>普通股每股面額</td>
            <td>員工人數(人)</td>
            <td></td>
            <td></td>
        </tr>
    </table>

   - 範例

    ``` python
    # 擷取台股上市上櫃 所有公司基本資訊
    >>> colist = ['股票代號', '股票名稱', '中文簡稱', '董事長', '總經理']
    >>> owlapp.cim(colist)

    [out]
        股票代號  股票名稱   中文簡稱   董事長   總經理
    0     1101     台泥       台泥     張安平   李鐘培
    1     1102     亞泥       亞泥     徐旭東   李坤炎
    2     1103     嘉泥       嘉泥     張剛綸   祁士鉅
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

10. 股利政策 個股 (Dividend Policy Single, DPS)

    <br>依據指定年度區間，撈取指定股票的配發股利狀況表
    <br>

    ``` python
    OwlData.dps(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

     - 欄位

    <table>
        <tr>
            <th colspan="5">免費版</th>
        </tr>
        <tr>
            <td>年度</td>
            <td>除息日</td>
            <td>除權日</td>
            <td>現金股利合計(元)</td>
            <td>股票股利合計(元)</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="4">付費版</th>
        </tr>
        <tr>
            <td>年度</td>
            <td>除息日</td>
            <td>除權日</td>
            <td>現金股利合計(元)</td>
        </tr>
        <tr>
            <td>股票股利合計(元)</td>
            <td>股利合計(元)</td>
            <td>盈餘配息(元)</td>
            <td>公積配息(元)</td>
        </tr>
        <tr>
            <td>盈餘配股(元)</td>
            <td>公積配股(元)</td>
            <td>領股日期</td>
            <td>領息日期</td>
        </tr>
        <tr>
            <td>現金股利殖利率(%)</td>
            <td>股票股利發放率(%)</td>
            <td>股利發放率(%)</td>
            <td>董監改選年度</td>
        </tr>
    </table>

     - 範例

    ```python
    # 擷取台積電股利政策資料 from 2017 to 2018
    >>> colist = ['年度', '除息日', '除權日', '現金股利合計(元)','股票股利合計(元)']
    >>> owlapp.dps("2330", "2017", "2018", colist)
    [out]
            年度        除息日     除權日  現金股利合計(元)  股票股利合計(元)
    0   2017-12-31    20180625                  8                0
    1   2018-12-31    20190624                  8                0
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

11. 股利政策 多股 (Dividend Policy Multi, DPM)

    <br>依指定年度，撈取全上市櫃台股的配發股利狀況表
    <br>

    ``` python
    OwlData.dpm(dt:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一年度 4碼，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

      - 欄位

    <table>
        <tr>
            <th colspan="4">免費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>除息日</td>
        </tr>
        <tr>
            <td>除權日</td>
            <td>現金股利合計(元)</td>
            <td>股票股利合計(元)</td>
            <td></td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="4">付費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>除息日</td>
        </tr>
        <tr>
            <td>除權日</td>
            <td>現金股利合計(元)</td>
            <td>股票股利合計(元)</td>
            <td>股利合計(元)</td>
        </tr>
        <tr>
            <td>盈餘配息(元)</td>
            <td>公積配息(元)</td>
            <td>盈餘配股(元)</td>
            <td>公積配股(元)</td>
        </tr>
        <tr>
            <td>領股日期</td>
            <td>領息日期</td>
            <td>現金股利殖利率(%)</td>
            <td>股票股利發放率(%)</td>
        </tr>
        <tr>
            <td>股利發放率(%)</td>
            <td>董監改選年度</td>
            <td></td>
            <td></td>
        </tr>
    </table>

      - 範例

    ``` python
    # 擷取台股上市上櫃  from 2018 所有股利政策資訊
    >>>　colist = ['股票代號', '股票名稱', '年度', '除息日','除權日','現金股利合計(元)', '股票股利合計(元)']
    >>> owlapp.dpm("2018", colist)
    [out]
        股票代號 股票名稱      年度       除息日      除權日   現金股利合計(元)  股票股利合計(元)
    0     1101    台泥    2018-12-31   20190813   20190813       3.31            0.70
    1     1102    亞泥    2018-12-31   20190724                  2.80            0.00
    2     1103    嘉泥    2018-12-31   20190829                  1.00            0.00
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

12. 除權除息 個股 (Exemption Dividend Policy Single, EDPS)

    <br>依據指定年度區間，撈取指定股票的股東會日期及停止過戶的相關日期
    <br>

    ``` python
    OwlData.edps(sid:str, bpd:str, epd:str, colist:list) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="4"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b>  bpd </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢起始年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> epd</b> : <i> string</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢結束年度 4 碼數字，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
            <th colspan="5">免費版</th>
        </tr>
        <tr>
            <td>年度</td>
            <td>停止過戶起</td>
            <td>停止過戶迄</td>
            <td>最後過戶日</td>
            <td>股東會日期</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="5">付費版</th>
        </tr>
        <tr>
            <td>年度</td>
            <td>停止過戶起</td>
            <td>停止過戶迄</td>
            <td>最後過戶日</td>
            <td>股東會日期</td>
        </tr>
        <tr>
            <td>停止融券起始日</td>
            <td>融券回補日</td>
            <td>停止融券終迄日</td>
            <td>停止融資起始日</td>
            <td>停止融資終迄日</td>
        </tr>
    </table>
    - 範例

    ``` python
    # 擷取台積電除權除息資料 from 2017 to 2018
    >>> colist = ['年度', '停止過戶起', '停止過戶迄', '最後過戶日','股東會日期']
    >>> owlapp.edps("2330", "2017", "2018", colist)

    [out]
            年度     停止過戶起   停止過戶迄    最後過戶日   股東會日期
    0   2017-12-31   20170410    20170608     20170407     20170608
    1   2018-12-31   20180407    20180605     20180403     20180605
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

13. 除權除息 多股 (Exemption Dividend Policy Multi, EDPM)

    <br>依指定日期，撈取全上市櫃台股的股東會日期及停止過戶的相關日期
    <br>

    ``` python
    OwlData.edpm(dt:str, colist:str) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> dt </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;查詢某一年度 4 碼，格式: yyyy
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>: 
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
            <th colspan="7">免費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>停止過戶起</td>
            <td>停止過戶迄</td>
            <td>最後過戶日</td>
            <td>股東會日期</td>
        </tr>
    </table>
    <table>
        <tr>
            <th colspan="4">付費版</th>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>年度</td>
            <td>停止過戶起</td>
        </tr>
        <tr>
            <td>最後過戶日</td>
            <td>停止過戶迄</td>
            <td>股東會日期</td>
            <td>停止融券起始日</td>
        </tr>
        <tr>
            <td>融券回補日</td>
            <td>停止融券終迄日</td>
            <td>停止融資起始日</td>
            <td>停止融資終迄日</td>
        </tr>
    </table>

    - 範例

    ``` python
    # 擷取台股上市上櫃  2018 所有除權除息資訊
    >>> colist = ['股票代號', '股票名稱', '年度','停止過戶起','停止過戶迄', '最後過戶日','股東會日期']
    >>> owlapp.edpm("2018", colist)

    [out]
        股票代號  股票名稱      年度      停止過戶起    停止過戶迄    最後過戶日   股東會日期
    0     1101     台泥    2018-12-31    20180424     20180622     20180423     20180622
    1     1102     亞泥    2018-12-31    20180428     20180626     20180427     20180626
    2     1103     嘉泥    2018-12-31    20180423     20180621     20180420     20180621
    ```

    <div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

14. 即時報價 (Timely Stock Price, TSP)

    <br>撈取指定股票即時股價資訊
    <br>

    ``` python
    OwlData.tsp(sid:str, colist:str) -> DataFrame
    ```

    <table>
        <tr>
            <td rowspan="2"><b>Parameters<b></td>
            <td> - <b> sid </b> : <i> string </i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;股票代號
            </td>
        </tr>
        <tr>
            <td> - <b> colist </b>:
            <i> list, default None</i>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp;指定顯示欄位 (若不輸入則顯示所有欄位)
            </td>
        </tr>
        <tr>
            <td><b> Returns</b></td><td>DataFrame or Series</td>
        </tr>
        <tr>
            <td colspan="2">
            <b> Note</b>
            <br>
                &nbsp;&nbsp;&nbsp;&nbsp; - 發生錯誤時，會直接顯示錯誤訊息，回傳變數為空
            </td>
        </tr>
    </table>

    - 欄位

    <table>
        <tr>
        <td colspan="7">付費版</td>
        </tr>
        <tr>
            <td>股票代號</td>
            <td>股票名稱</td>
            <td>時間</td>
            <td>成交價</td>
            <td>漲跌</td>
            <td>漲跌幅</td>
        </tr>
        <tr>
            <td>總量</td>
            <td>開盤價</td>
            <td>最高價</td>
            <td>最低價</td>
            <td>成交量</td>
        </tr>
    </table>

    - 範例

    ``` python
    # 擷取台積電即時報價
    >>> colist = ['股票代號', '股票名稱', '時間', '開盤價', '最高價', '最低價', '成交量']
    >>> owlapp.tsp("2330", colist)

    [out]
        股票代號    股票名稱	      時間	開盤價	最高價	最低價	成交量
    0     2330	台積電	20190814143000	252.50	254.00	249.50	 11.00
    ```

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>

## Notes

- Python 免費版資料期間限制於2年，欄位詳見 GitHub或數據貓頭鷹官網

- 免費版試用期間為 90 日，過期則需要再等 2 日才能再次申請免費試用

- Python 付費版資料期間為 10 年，欄位詳見 GitHub或數據貓頭鷹官網

- 若付費本出現無法擷取資料的情況，可能是因為商品清單或是交易週期對應表過期所導致，請向客服進行聯繫 (預設過期天數為999天，等待期限 1 日)

**有任何相關錯誤請聯繫:**

- E-mail：service@cmoney.com.tw
- 請撥打 02-8252-6620 分機241
- 星期一-星期五: 早上9:00-下午6:00, 除了國定假日以外

## Contribute

owldata was created by OwlData co. <owldb@cmoney.com.tw>

Contributing were welcome, please use GitHub issue and Pull Request to contribute!

歡迎協作，請使用 GitHub issue 以及 Pull Request 功能來協作。

<div style="text-align: right"> <a href = #owldata-%e6%95%b8%e6%93%9a%e8%b2%93%e9%a0%ad%e9%b7%b9-api> top </a> </div>