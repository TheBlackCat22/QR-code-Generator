def main():


    from googleapiclient.http import MediaFileUpload
    from Google import Create_Service
    import qrcode
    from tkinter.filedialog import askopenfilename
    import pandas as pd
    from os.path import exists


    CLIENT_SECRET_FILE = "client_secret.json"
    API_NAME="drive"
    API_VERSION="v3"
    SCOPES=["https://www.googleapis.com/auth/drive"]


    service=Create_Service(CLIENT_SECRET_FILE,API_NAME,API_VERSION,SCOPES)


    folder_id="18C4heZLU1LbUTBuY-cxwoACVIJ7xx_CP"
    pic_path=askopenfilename()
    name=input("Enter Owner Name: ")
    roll_no=input("Enter Owner Roll Number: ")
    pic_name=name+"_"+roll_no


    pic_metadata={
        'name':pic_name,
        'parents':[folder_id]
    }

    pic_media = MediaFileUpload(pic_path, mimetype="image/jpeg")

    pic_id = service.files().create(
        body=pic_metadata,
        media_body=pic_media,
        fields="id"
    ).execute().get('id')


    request_body = {
        'role': 'reader',
        'type': 'anyone'
    }

    service.permissions().create(
        fileId=pic_id,
        body=request_body
    ).execute()

    link = service.files().get(
        fileId=pic_id,
        fields='webViewLink'
    ).execute().get('webViewLink')


    if exists("Details.csv"):
        df=pd.read_csv("Details.csv")
    else:
        df=pd.DataFrame(columns=["Name","Roll Number","Id Link"])
    temp={"Name":name,"Roll Number":roll_no,"Id Link":link}
    df=df.append(temp,ignore_index=True)
    df.to_csv("Details.csv",index=None)


    csv_id="18C4heZLU1LbUTBuY-cxwoACVIJ7xx_Cs"
    csv_media=MediaFileUpload("Details.csv",mimetype="text/csv")
    service.files().update(
        fileId=csv_id,
        media_body=csv_media
    ).execute()


    qr=qrcode.make(link)
    qr.save(pic_name+".png")

       
if __name__ == "__main__":
    main()

