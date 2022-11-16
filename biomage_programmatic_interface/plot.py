class Plot:
    def __init__(self, connection):
        self.connection = connection

    def __get_upload_url(self, experiment_id):
        url = f'v2/customPlots/{experiment_id}/imageUploadUrl'
        response = self.connection.fetch_api(url, {}, method='GET')
        return response.content.decode('UTF-8')

    def upload_image(self, experiment_id, img_path):
        s3url = self.__get_upload_url(experiment_id)
        self.connection.upload_to_S3(s3url, img_path)