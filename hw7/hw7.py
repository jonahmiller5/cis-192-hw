'''
Name: Jonah Miller
PennKey: jonahmil
Hours of work required: 6
'''

'''
In some functions below, the keyword "pass" is used to
indicate to the interpreter that the corresponding codeblock
is empty. This is necessary in order for the interpreter
not to consider empty code blocks as syntax errors.
You will replace each of these "pass" keywords by your
code completing the function as described in the comments.
'''

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import matplotlib.pyplot as plt
from itertools import cycle
import numpy as np
import torchvision.transforms as transforms


class ReshapeTransform:
    '''
    We will use this class for transforming an input tensor
    to a different shape. This will later be passed into
    the torchvision.transforms.Compose transformer.
    '''
    def __init__(self, new_size):
        '''
        Initialize the transformer. You just need to store
        the new_size.
        args:
            new_size: a tuple with the shape to which tensors
            will be transformed
        ret: None
        '''
        self.size = new_size

    def __call__(self, img):
        '''
        Transform the input tensor into the new_size. This function
        is called by the data loader if you pass in ReshapeTransform
        as a transformation. You may also create a ComposedTransform
        with a list of transformations from torchvision and ReshapeTransform
        args:
            img: an input tensor
        ret:
            reshaped_img: a tensor with the data of img
            and the shape new_size
        Note: you may assume img and new_size are compatible
        '''

        result = torch.reshape(img, self.size)

        return result


def load_data(root='./data'):
    '''
    Load the MNIST data using torchvision and apply the appropriate
    transformations
    args:
        root: the directory from which data will be loaded
    ret:
        trainloader: a torch.utils.DataLoader for the trainset
        testloader: like trainloader for the testset
    '''
    r_transform = ReshapeTransform((-1,))
    transform = transforms.Compose([transforms.ToTensor(), r_transform])

    trainset = torchvision.datasets.MNIST(root=root, train=True,
                                          download=True, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=10,
                                              shuffle=True, num_workers=4)
    testset = torchvision.datasets.MNIST(root=root, train=False,
                                         download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=10,
                                             shuffle=False, num_workers=4)

    return trainloader, testloader


def create_fnn(in_size, num_classes):
    '''
    Create a fully connected network as specified in the
    write-up (two hidden linear layers with 64 units, each
    followed by ReLU activation)
    args:
        in_size: size of input (int)
        num_classes: number of output nodes (int)
    ret:
        fnn: the fully connected network whose input is of
        size in_size and output is of size num_classes
    Note: there are 2 *hidden* layers. This means there must
    be an additional third layer for the output
    '''
    fc1 = nn.Linear(in_size, 64)
    fc2 = nn.Linear(64, 64)
    fc3 = nn.Linear(64, num_classes)

    return nn.Sequential(fc1, nn.ReLU(), fc2, nn.ReLU(), fc3)


def train_fnn(net, trainloader, testloader):
    '''
    Train the network net on data from the trainloader.
    Recall the high-level algorithm:
    For each epoch
        For each minibatch
            compute the output predictions
            compute the loss
            zero the gradients
            backpropagate
            use the optimizer to take a step
    In this function, you will keep track of the running
    average of the train and test losses and accuracies,
    over windows of 2,000 iterations.
    args:
        net: a neural network (e.g., constructed via nn.Sequential)
        trainloader, testloader: the data loaders for train and
        test set
    ret:
        loss_train: a list of the training loss averages (one for
        each 2,000 iterations)
        loss_test: a list of the test loss averages (one for each
        2,000 iterations)
        acc_train: a list of the training accuracy averages (one for
        each 2,000 iterations)
        acc_test: a list of the training accuracy averages (one for
        each 2,000 iterations)
    '''
    loss_fn = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters())

    loss_train = []
    loss_test = []
    acc_train = []
    acc_test = []
    for epoch in range(2):
        running_training_loss = 0.0
        running_testing_loss = 0.0
        correct_train = 0.0
        correct_test = 0.0
        total_train = 0.0
        total_test = 0.0
        for i, data in enumerate(zip(trainloader, cycle(testloader))):
            training, testing = data

            training_inputs, training_labels = training
            testing_inputs, testing_labels = testing

            optimizer.zero_grad()

            training_outputs = net(training_inputs)
            testing_outputs = net(testing_inputs)
            training_loss = loss_fn(training_outputs, training_labels)
            testing_loss = loss_fn(testing_outputs, testing_labels)

            training_loss.backward()

            optimizer.step()

            running_training_loss += training_loss.item()
            running_testing_loss += testing_loss.item()

            with torch.no_grad():
                _, training_predicted = torch.max(training_outputs.data, 1)
                _, testing_predicted = torch.max(testing_outputs.data, 1)
                total_train += training_labels.size(0)
                total_test += testing_labels.size(0)
                correct_train += (training_predicted ==
                                  training_labels).sum().item()
                correct_test += (testing_predicted ==
                                 testing_labels).sum().item()
                train_accuracy = 100 * correct_train / total_train
                test_accuracy = 100 * correct_test / total_test

            if i % 2000 == 1999:
                loss_train.append(running_training_loss / 2000)
                loss_test.append(running_testing_loss / 2000)
                acc_train.append(train_accuracy)
                acc_test.append(test_accuracy)

                running_training_loss = 0.0
                running_testing_loss = 0.0
                train_accuracy = 0.0
                total_train = 0
                correct_train = 0
                test_accuracy = 0
                correct_test = 0
                total_test = 0

    return loss_train, loss_test, acc_train, acc_test


def plot_results(loss_train, loss_test, acc_train, acc_test):
    '''
    Create a plot with two subplots. The top one should contain the
    loss plot, with a line for the training loss and a line for the
    test loss. The bottom one should contain the accuracy plot, also
    for train and test
    args:
        loss_train: a list of the training loss averages (one for
        each 2,000 iterations)
        loss_test: a list of the test loss averages (one for each
        2,000 iterations)
        acc_train: a list of the training accuracy averages (one for
        each 2,000 iterations)
        acc_test: a list of the training accuracy averages (one for
        each 2,000 iterations)
    ret: None
    Outcome: the plot should be saved to "MNISTLearningCurves.pdf"
    '''
    x_delim = [0, 2000, 4000, 6000, 8000, 10000]
    plt.figure()
    plt.suptitle('Training and Testing Loss and Accuracy')
    fig, axs = plt.subplots(2)

    axs[0].plot(x_delim, loss_train, label="Training")
    axs[0].plot(x_delim, loss_test, label="Testing")
    axs[0].set(ylabel="Loss")
    axs[0].legend()

    axs[1].plot(x_delim, acc_train)
    axs[1].plot(x_delim, acc_test)
    axs[1].set(xlabel="Iterations", ylabel="Accuracy")

    plt.savefig('MNISTLearningCurves.pdf')


def main():
    '''
    Use this for testing!
    '''
    trainloader, testloader = load_data()
    net = create_fnn(784, 10)
    loss_train, loss_test, acc_train, acc_test = train_fnn(net,
                                                           trainloader,
                                                           testloader)
    plot_results(loss_train, loss_test, acc_train, acc_test)

if __name__ == '__main__':
    '''
    This calls the function main() when executing python3 hw6.py
    '''
    main()
