'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 3
'''

'''
In some functions below, the keyword "pass" is used to
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.
'''

from sklearn.cluster import KMeans
from PIL import Image
import numpy as np


def load_image(filename):
    '''
    Load an image from file into a numpy array
    args:
        filename: a string with the path to the file
    ret:
        data: a numpy array of shape height x width x 3
        representing the rows, columns, and colors of an
        RGB image
    '''
    img = Image.open(filename)
    img.load()
    data = np.asarray(img, dtype='uint8')
    return data


def save_image(imarr, filename):
    '''
    Save an array representing an image to file
    args:
        imarr: an array representing the image. Must be
        type unit8
    ret: None
    Outcome:
        The image is saved to file
    '''
    img = Image.fromarray(imarr, 'RGB')
    img.save(filename)


def from_imarr_to_dataset(imarr):
    '''
    Create a data set from imarr. The data set should
    be a numpy array whose rows correspon d to pixels
    and the columns correspond to R, G, B, X, Y
    args:
        imarr: an array representing the image of shape
        h x w x 3
    ret:
        X: the resulting data set of shape (hw) x 5
    Hint:
        Avoiding looping in this function requires some
        thought! You might find the np.tile function
        useful
    '''
    coords = np.dstack(np.indices((imarr.shape[0], imarr.shape[1])))
    matrix = np.concatenate((imarr, coords), axis=2)
    matrix = np.concatenate(matrix, axis=0)
    return matrix


def cluster_data(X):
    '''
    args:
        X: the data set of shape (hw) x 5
    ret:
        y: the cluster assignments of shape hw
        model: a fitted scikit-learn k-means model
    '''
    model = KMeans(n_clusters=20)
    model.fit(X)
    return model.labels_, model


def create_segmented_image(shape, model, X, y):
    '''
    Create an image whose pixel values correspond to the
    colors of the cluster centroids assigned to each pixel
    in the original image.
    args:
        shape: a tuple with the original shape of the image
        (h x w x 3)
        model: a fitted scikit-learn k-means model
        X: the data set of shape (hw) x 5
        y: the cluster assignments of shape hw
    ret:
        img: numpy array representing the segmented image.
        Must be of shape=shape. The color of each pixel
        should match the color of the cluster centroid to
        which the pixel is assigned
    Note: you should not assume that the data set is in the
    same order as when you processed it! You should leverage
    X to find where the original pixel was located. This
    might require some clever indexing.
    '''
    centers = model.cluster_centers_
    colors = centers[y].astype(np.uint8)
    colors = colors[:, :3]
    image = np.zeros(shape, dtype=np.uint8)
    image[X[:, 3], X[:, 4]] = colors

    return image


def main():
    '''
    Use this for testing!
    '''
    im = load_image('flowers.jpg')
    '''Follow steps 2--4 here'''
    d = from_imarr_to_dataset(im)
    labels, model = cluster_data(d)
    im_transformed = create_segmented_image(im.shape, model, d, labels)
    save_image(im_transformed, 'kmeans_flowers.jpg')


if __name__ == '__main__':
    '''
    This calls the function main() when executing python3 hw6.py
    '''
    main()
