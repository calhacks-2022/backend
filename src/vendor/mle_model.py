import sys
sys.path.insert(0, 'src/vendor')
import pickle
import numpy as np

class GaussianModel():
    def __init__(self):
        self.random_projection = None
        self.cov = None
        self.mean = None
        self.num_packages = None
    
    def train(self, pkgs, pkg_samples):
        num_packages = len(pkgs)
        self.num_packages = num_packages
        print(num_packages)
        encoded_data = np.zeros((len(pkg_samples), num_packages))
        for i in range(len(pkg_samples)):
            encoded_data[i][list(pkg_samples[i])] = 1
        self.random_projection = GaussianRandomProjection(n_components=120).fit(encoded_data).components_
        transformed_data = encoded_data @ self.random_projection.T
        self.cov = np.cov(transformed_data.T)
        self.mean = np.mean(transformed_data, axis=0)
        self.cov_inv = np.linalg.inv(self.cov)
    
    def log_likelihood(self, encoding):
        return (encoding - self.mean) @ (self.cov_inv @ (encoding - self.mean))
    
    def recommend_package(self, pkgs, recs):
        new_pkgs = np.zeros(self.num_packages)
        new_pkgs[pkgs] = 1
        ret = []
        for rec in recs:
            '''
            if rec == 1608:
                print('good')
            if pkgs[rec] == 1:
                return rec
            '''
            pkgs_copy = new_pkgs.copy()
            pkgs_copy[rec] += 1
            transformed_pkgs = pkgs_copy @ self.random_projection.T
            score = self.log_likelihood(transformed_pkgs)
            ret.append((score, rec))
        ret = sorted(ret)
        return ret
    
    def save_model(self, name='gaussian_model.pkl'):
        pickle.dump(self, open(name, 'wb'))

    def load_model(name='gaussian_model.pkl'):
        return pickle.load(open(name, 'rb'))