import requests
from requests_html import HTML
import json
import pdfkit
import pytesseract
import io
import os
from PIL import Image
from random import randint

html=""
captcha = ""

ocr_space_api_key = "xxxxxxxxxxxxxx" # Enter Your API key of https://ocr.space/OCRAPI, its required to automate image captcha


try:
    api_key = os.environ["OCR_API"]
except:
    api_key = ocr_space_api_key



def web_req(url , engine, timeout): #accepts captcha url and engine and returns solved text

        payload={
                'apikey':api_key,
                'OCREngine':engine,
                'url':url
                }
        res=requests.post("https://api.ocr.space/Parse/Image" , data=payload , timeout=timeout)
        res_json=json.loads(res.text)

        try:
                text=res_json.get('ParsedResults')[0].get('ParsedText')
                text=text.replace(" ","")
                text=text.upper()
                text=text.replace("\n" , "")
                text=text.replace("\t" , "")
                return text

        except:
                return res.text


def solve_captcha(url):
        try:
                captcha=web_req(url,2,5)
                if len(captcha) != 5:
                        captcha=web_req(url,5,4)
                return captcha
        except:
                global html
                html=rgpv_html()
                url=get_captcha_url(html)
                print("Solving Captcha..again.")
                try:
                        captcha=web_req(url,2,5)
                except:
                        res=requests.get(url)
                        img = Image.open(io.BytesIO(res.content))
                        captcha=pytesseract.image_to_string(img , timeout=3)
                        captcha=captcha.replace(" ","")
                        captcha=captcha.upper()
                        captcha=captcha.replace("\n" , "")
                        captcha=captcha.replace("\t" , "")
                return captcha


cookie=""

def rgpv_html(): #takes nothing returns rgpv html
        res=requests.get("http://result.rgpv.ac.in/Result/ProgramSelect.aspx")
        html=HTML(html=res.text)
        viewstate=html.find('#__VIEWSTATE')[0].attrs["value"]
        eventvalidation=html.find('#__EVENTVALIDATION')[0].attrs["value"]
        payload={
        '__EVENTTARGET':'radlstProgram$1',
        '__EVENTARGUMENT':'',
        '__LASTFOCUS':'',
        '__VIEWSTATE':viewstate,
        '__VIEWSTATEGENERATOR':'F697B5F5',
        '__EVENTVALIDATION':eventvalidation,
        'radlstProgram':'24'
        }

        res=requests.post("http://result.rgpv.ac.in/Result/ProgramSelect.aspx" , data=payload)

        global cookie
        cookie=res.history[0].headers["Set-Cookie"].replace("; path=/; HttpOnly","")
        html=HTML(html=res.text)
        return html




def get_captcha_url(html):  #takes rgpv html returns captcha url
        url=html.find('table.gridtable')[1].find('tr')[0].find('td')[0].find('div')[0].find('img')[0].attrs["src"]

        url='http://result.rgpv.ac.in/Result/'+url
        return url


def get_result(enrollment, semester, captcha, html):

        viewstate=html.find('#__VIEWSTATE')[0].attrs["value"]
        eventvalidation=html.find('#__EVENTVALIDATION')[0].attrs["value"]

        global cookie
        headers={'Cookie':cookie}

        payload={


        '__EVENTTARGET':'',
        '__EVENTARGUMENT':'',
        '__VIEWSTATE':viewstate ,
        '__VIEWSTATEGENERATOR':'56D9EF13',
        '__EVENTVALIDATION':eventvalidation ,
        'ctl00$ContentPlaceHolder1$txtrollno':enrollment ,
        'ctl00$ContentPlaceHolder1$drpSemester':semester ,
        'ctl00$ContentPlaceHolder1$rbtnlstSType':'G',
        'ctl00$ContentPlaceHolder1$TextBox1':captcha ,
        'ctl00$ContentPlaceHolder1$btnviewresult':'View Result'

        }


        res=requests.post("http://result.rgpv.ac.in/Result/BErslt.aspx" ,headers=headers, data=payload ,verify=False)

        return res.text

def get_result_details(html):
        try:
               
                if html.find("div.rslmain")[0].text.split("\n")[17].split('");')[0].replace('alert("' , '') == 'Result for this Enrollment No. not Found':
                        # print("Result for this Enrollment No. not Found")
                        return "Result for this Enrollment No. not Found"
                elif html.find("div.rslmain")[0].text.split("\n")[19].split('");')[0].replace('alert("' , '') == 'you have entered a wrong text':
                        print("Wrong Captcha")
                        return "Some error occurred, Please try again /result"
                else:

                        NAME=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[0].text.split("\n")[2]
                        ENROLLMENT=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[0].text.split("\n")[4]
                        TIME=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[0].text.split("\n")[0].split("\xa0- ")[1]
                        COURSE=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[0].text.split("\n")[6]
                        BRANCH=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[0].text.split("\n")[8]
                        SEMESTER=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[0].text.split("\n")[10]
                        STATUS=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[0].text.split("\n")[12]
                        elem = html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')
                        index_of_desc = len(elem) - 2

                        if int(SEMESTER) >= 7:
                                DESC= html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[index_of_desc].text.split("\n")[3]
                                SGPA=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[index_of_desc].text.split("\n")[4]
                                CGPA=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[index_of_desc].text.split("\n")[5]


                        else:
                                DESC= html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[index_of_desc].text.split("\n")[3]
                                SGPA=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[index_of_desc].text.split("\n")[4]
                                CGPA=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[index_of_desc].text.split("\n")[5]

                        heder=f'**Name** - `{NAME}`\n**Roll No.** - `{ENROLLMENT}`\n**Session** - `{TIME}`\n**Course** - `{COURSE}`             **Branch** - `{BRANCH}`\n**Semester** - `{SEMESTER}`                    **Status** - `{STATUS}`\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬' #UPPER PART NAME ENROLL ETC
                        all_list=[]
                        if int(SEMESTER) >= 7:
                                rng_limit = 8
                        elif int(SEMESTER) >= 5:
                                rng_limit = 11
                        else:
                                rng_limit = 12

                        for x in range(2,rng_limit):
                                all_list.append(html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('table.gridtable')[x].text.split("\n"))

                        table=f'Subject               Total     Earned      Grade**\n' #MIDDLE GRADE table
                        for x in all_list:
                                table+=f'`{x[0]}`         {x[1]}           {x[2]}                {x[3]}**\n'

                        footer=f'▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n**Result Des.** - `{DESC}`🙈\n**SGPA** - `{SGPA}` 🎉                **CGPA** - `{CGPA}` 🎉\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬' #lower part SGPA CGPA ETC...

                        text=f'{heder}\n\n{table}\n{footer}'
                        return text
        except Exception as m:
                print(f"{m} Something Went wrong while parsing result")
                error = "Some error occurred, Please try again /result"
                return error




def generate_pdf(html , enrollment): #accepts html + enrollment and returns boolean if pdf successfully generated

        footer=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].find('#ctl00_ContentPlaceHolder1_LinkButton1Grading')[0].html

        footer_2=html.find("div.footer-copyright")[0].html

        body=html.find('#ctl00_ContentPlaceHolder1_pnlGrading')[0].html.replace(footer,"").replace(footer_2,"").replace("\xa0"," ")

        style='<style>body{font-family:Verdana, Arial;font-size:12px;color:#333333;line-height:1.166;margin:0px;padding:5px 0px 0px 0px;background-color:#EBEEF3;}img{border:0px;}p{font-family:Verdana, Arial;font-size:12px;color:#333333;line-height:18px;padding:5px 3px 3px 5px;text-align:justify;}.Normaltext{font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#963;font-weight:700;}.FieldText{font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#000;background-color:#CAE8EA;font-weight:700;border:thin solid #CCC;}.lightcolorField{font-family:Arial, Helvetica, sans-serif;font-size:12px;color:#963;background-color:#FFFAEA;font-weight:700;border:thin solid #CCC;}.resultText{font-family:arial;font-size:12px;font-weight:700;color:#000;border:thin solid #CCC;}table.gridtable{font-family:verdana,arial,sans-serif;font-size:11px;color:#333333;border-width:1px;border-color:#666666;border-collapse:collapse;}table.gridtable th{border-width:1px;padding:8px;border-style:solid;border-color:#666666;background-color:#dedede;}table.gridtable td{border-width:1px;padding:8px;border-style:solid;border-color:#666666;background-color:#ffffff;}.rslmain{border:8px #FFF solid; background-color:#FFFFFF; width:950px; margin:0 auto;}     .header-wrapper{ background:#97d4fc; height:auto; width:100%; border-bottom:#d9281e 4px solid; border-top:#7aa4cd 8px solid;}.logo_contain {text-align: center; vertical-align:middle; padding:10px 0px 10px 0px; float:left;}.name_contain {text-align: center; height:100px; margin-left: 55px; padding-top:15px; font-family:Tahoma, Arial, Helvetica, sans-serif; color:#114C88; font-size:24px; font-weight:bold; line-height:34px;} .name_contain span {font-family:Verdana,Monotype Corsiva; color:#ED1C24; font-size:24px; font-weight:bold;  line-height:34px;}.name_contain .mis {text-align:right; font: 10pt Tahoma; font-weight: bold; line-height:normal; padding-bottom:5px; padding-right:10px;}.name_contain .mis a{color:#0373BD; text-decoration:none;}.name_contain .mis a:hover{color:#FFFFFF;}.rslcenter{background-color:#FFF; text-align:center; vertical-align:middle; min-height:480px;}.footer-copyright{background-color:#3f678e;  vertical-align:middle; text-align:center; padding:10px 0px; border-top:2px solid #18334d; border-bottom:2px solid #18334d;}.footer-copyright .copyright{ font-size:11px; color:#FFF;}.footer-copyright .copyright a{color:#52def5;}.resultheader{background:#f9f4d6; height:90px; border:#bcb58b 1px solid; text-align:center; font-family:Tahoma, Arial, Helvetica, sans-serif; color:#302603; font-size:24px; font-weight:bold; line-height:34px;}</style>'

        watermark = '<div id="watermark">Downloaded from - <b>http://t.me/rgpv_results_bot</b></div><style>#watermark { position: fixed; bottom: 5; right: 5; z-index:999; }</style>'

        pdf_body=f'<html><center> {style}{body} </center>{watermark}</html>'

        return pdfkit.from_string(pdf_body, f'pdf/{enrollment}.pdf')





def pre_result():
        global html , captcha
        html=rgpv_html()
        url=get_captcha_url(html)
        print("Solving Captcha...")
        captcha=solve_captcha(url)
        print("Here is solved captcha: " , captcha)

def post_result(enrollment,semester):
        global html
        result=get_result(enrollment, semester, captcha, html)
        print("\n")
        print("\n")
        # with open("wrong_captcha.html","w") as file:   # save html locally for further inspection 
        #     file.write(result)
        # html=HTML(html=result)
        try:
                result=get_result_details(html)
                if len(result) >= 50:
                        generate_pdf(html, enrollment)
                        print("DONE....")
                        return result
                else:
                        print(result)
                        return result

        except Exception as c:
                print(f"c {c} Some Error Occoured During Parsing Result...")



#FOR TESTING
#pre_result()
#input("Enter something: ")
#print(post_result("0601EC201021","4"))
