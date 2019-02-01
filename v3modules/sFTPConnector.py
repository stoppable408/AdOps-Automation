
class sFTPConntector():

    def __init__(self):
        import pysftp
        self.pysftp = pysftp
        self.host = "sftp.aemedia.us"
        self.username = "GMAdOps500"
        self.password = "P@ssw0rd1"
        self.port = 22
        pass

    def uploadFile(self, filename, foldername):
        cnopts = self.pysftp.CnOpts()
        cnopts.hostkeys = None   
        with self.pysftp.Connection(self.host, username=self.username, password=self.password, cnopts=cnopts) as sftp:
            with sftp.cd(foldername):
                sftp.put(filename)  	# upload file to allcode/pycode on remote
            # sftp.get('remote_file')    


# test = sFTPConntector()
# test.connect()