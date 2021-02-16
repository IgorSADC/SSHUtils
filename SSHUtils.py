from functools import partial
import os
from SecurePathProxy import SecurePathProxy

class SSHUtils:
    '''
    This is a class of utilities that I use on my remote workflow.
    '''
    def __init__(self, sshconnection):
        self.sshconnection = sshconnection
        self.sftp_client = self.sshconnection.open_sftp()
        self.current_remote_directory = self.sftp_client.getcwd()
        self.current_directory = os.getcwd()
               
        
    def download_file(self, file_path, local_path = ".", current_path = None):
      #  if(current_path != None):
      #      base_path = local_path.split(os.path.basename(local_path))[0]
      #      self.make_folder_if_necessary(os.path.join(base_path, current_path), os_entity = os)
      #      local_path = os.path.join(base_path, current_path, os.path.basename(local_path))
                                      
        return self.sftp_client.get(file_path, local_path)
        
    def upload_file(self, file_path, remote_path = '.', current_path = None):
       # if(current_path != None):
       #     self.make_folder_if_necessary(remote_path, os_entity = self.sftp_client)
       #     remote_path = current_path
        return self.sftp_client.put(file_path, remote_path)
    
    def make_folder_if_necessary(self, path, os_entity):
        if path == '.': return
        try:
            os_entity.mkdir(path)
        except:
            return
        
    def change_remote_path(self, new_path):
        try:
            self.sftp_client.listdir(new_path)
            self.sftp_client.chdir(new_path)
            
        except:
            raise ValueError("Please enter a valid path")
            
    def ls(self, path='.'):
        return self.sftp_client.listdir(path)
    
    def get_files_by_extension(self, extension, os_entity, path ='.'):
        return [a for a in os_entity.listdir(path) if a.split('.')[-1] == extension]
    
    def get_filtered_files_by_extension(self, extension, os_entity, file_filter, path ='.'):
        return [a for a in os_entity.listdir(path) if a.split('.')[-1] == extension and file_filter(a)]
    
    def download_all_files_from_extension(self, extension, local_path ='.', remote_path = '.', file_filter = None, **kwargs):
        with SecurePathProxy(self.sftp_client, remote_path) as path_manager:
            file_list = self.get_files_by_extension(extension, self.sftp_client) if not callable(file_filter) else self.get_filtered_files_by_extension(extension, self.sftp_client, file_filter)
            for p in file_list:
                self.download_file(p, os.path.join(local_path, p), **kwargs)
                
    def upload_all_files_from_extension(self, extension, local_path = '.', remote_path = '.', file_filter = None, **kwargs):
        with SecurePathProxy(os, local_path):
            file_list = self.get_files_by_extension(extension, os) if not callable(file_filter) else self.get_filtered_files_by_extension(extension, os, file_filter)
            for p in file_list:
                self.upload_file(p, os.path.join(remote_path, p), **kwargs)
                
    def apply_function_recursivilly(self, function):
        with SecurePathProxy(self.sftp_client, '.') as path_manager:
            path_manager.apply_callable_entity_recursivily(function)
            
    def download_files_recursivilly(self, extension, local_path = '.', root_folder ='.', file_filter = None):
        func = partial(self.download_all_files_from_extension, extension = extension, remote_path = root_folder, local_path = local_path, file_filter = file_filter)
        self.apply_function_recursivilly(func)
        
    def upload_files_recursivilly(self, extension, local_path = '.', root_folder ='.', file_filter = None):
        func = partial(self.upload_all_files_from_extension, extension = extension, remote_path = root_folder, local_path = local_path, file_filter = file_filter)
        self.apply_function_recursivilly(func)
        
        