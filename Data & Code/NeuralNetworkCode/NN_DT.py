from keras.layers import Input, Dense, Activation, Dropout, BatchNormalization
from keras.layers.merge import Maximum, Concatenate
from keras.models import Model, Sequential
from keras.optimizers import Adam
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn import linear_model, svm, tree
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plot
import numpy as np

def build_generator():
    example = Input(shape=(1810,))
    noise = Input(shape=(20,))
    input = Concatenate(axis=1)([example, noise])
    x = Dense(256, activation="relu")(input)
    x = BatchNormalization()(x)
    x = Dense(1810, activation="sigmoid")(x)
    generator = Model([example,noise],x,name="generator")
    #generator.compile(loss="binary_crossentropy", optimizer="adam")
    return generator

def build_discriminator():
    input = Input(shape=(1810,))
    x = Dense(256, activation = "relu")(input)
    x = Dense(1, activation="sigmoid")(x)
    discriminator = Model(input,x,name="discriminator")
    #discriminator.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]) 
    return discriminator
    
def build_BB_DT():
    BB = tree.DecisionTreeRegressor()
    return BB
    
def load_data():
    mal_data = np.loadtxt("m_Encoded.csv", delimiter=",")
    ben_data = np.loadtxt("b_Encoded.csv", delimiter=",")
    x_mal = mal_data[:,0:1810]
    y_mal = mal_data[:,1810]
    x_ben = ben_data[:,0:1810]
    y_ben = ben_data[:,1810]
    return(x_mal, y_mal), (x_ben, y_ben)
    
def build_combined(discriminator, generator):
    discriminator.trainable=False
    example = Input(shape=(1810,))
    noise = Input(shape=(20,))
    input = [example, noise]
    adverse_examples = generator(input)
    validity = discriminator(adverse_examples)
    gan = Model(input, validity)
    gan.compile(loss="binary_crossentropy", optimizer="adam") 
    return gan

def training(epochs = 50, batch_size = 48):
    g = build_generator()
    d = build_discriminator()
    d.compile(loss="binary_crossentropy", optimizer="adam", metrics=["accuracy"]) 
    gan = build_combined(d, g)
    bb = build_BB_DT() 
    
    (x_mal, y_mal), (x_ben, y_ben) = load_data()
    x_mal_train, x_mal_test, y_mal_train, y_mal_test = train_test_split(x_mal, y_mal, test_size = 0.2)
    x_ben_train, x_ben_test, y_ben_train, y_ben_test = train_test_split(x_ben, y_ben, test_size = 0.2)
    gen_x_mal_train, bb_x_mal_train, gen_y_mal_train, bb_y_mal_train = train_test_split(x_mal_train, y_mal_train, test_size =0.5)
    gen_x_ben_train, bb_x_ben_train, gen_y_ben_train, bb_y_ben_train = train_test_split(x_ben_train, y_ben_train, test_size =0.5)
    #Train Detector
    bb.fit(np.concatenate([x_mal, x_ben]), np.concatenate([y_mal, y_ben]))
    y_ben_train_BB = bb.predict(bb_x_ben_train)
    Train_TPR_1 = bb.score(bb_x_mal_train, bb_y_mal_train)
    Test_TPR_1 = bb.score(x_mal_test, y_mal_test)
    Train_TPR, Test_TPR = [Train_TPR_1], [Test_TPR_1]
    best_TPR = 1.0
    
    for run in range(epochs):
        for train in range(gen_x_mal_train.shape[0] // batch_size):
            #Train Discriminator
            d.trainable=True
            i = np.random.randint(0, gen_x_mal_train.shape[0], batch_size)
            x_mal_set = gen_x_mal_train[i]
            noise = np.random.uniform(0,1,(batch_size, 20))
            i = np.random.randint(0, x_mal_set.shape[0], batch_size)
            x_ben_set = gen_x_ben_train[i]
            y_ben_set = y_ben_train_BB[i]
            adv_examples = g.predict([x_mal_set, noise])
            y_mal_set = bb.predict(np.ones(adv_examples.shape)*(adv_examples > 0.5))
            d_loss_mal = d.train_on_batch(adv_examples, y_mal_set)
            d_loss_ben = d.train_on_batch(x_ben_set, y_ben_set)
            d_loss = 0.5 * np.add(d_loss_mal, d_loss_ben)
            d.trainable=False
            #Train Generator
            i = np.random.randint(0, gen_x_mal_train.shape[0], batch_size)
            x_mal_set = gen_x_mal_train[i]
            noise = np.random.uniform(0, 1,(batch_size, 20))
            g_loss = gan.train_on_batch([x_mal_set, noise], np.zeros((batch_size, 1)))
        #Train TPR
        noise = np.random.uniform(0,1, (gen_x_mal_train.shape[0], 20))
        adv_examples = g.predict([gen_x_mal_train, noise])
        TPR = bb.score(np.ones(adv_examples.shape) * (adv_examples > 0.5), gen_y_mal_train)
        Train_TPR.append(TPR)
        #Test TPR
        noise = np.random.uniform(0,1, (x_mal_test.shape[0], 20))
        adv_examples = g.predict([x_mal_test, noise])
        TPR = bb.score(np.ones(adv_examples.shape) * (adv_examples > 0.5), y_mal_test)
        Test_TPR.append(TPR)
        
        if TPR < best_TPR:
            gan.save_weights("GanDT.h5")
            best_TPR = TPR
            
        print("%d[Discrimnator Loss: %f, Accuracy: %.2f%%][Generator Loss: %f]" % (run,d_loss[0], 100*d_loss[1], g_loss))
            
    #print('\n\n---{0}{1}'.format(bb))
    print('\nOriginal_Train_TPR:{0}, Adver_Train_TPR:{1}'.format(Train_TPR_1, Train_TPR[-1]))
    print('\nOriginal_Test_TPR:{0}, Adver_Tese_TPR:{1}'.format(Test_TPR_1, Test_TPR[-1]))
    #Plot TPR
    plot.figure()
    plot.plot(range(len(Train_TPR)), Train_TPR, c='r', label='Training Set', linewidth=2)
    plot.plot(range(len(Test_TPR)), Test_TPR, c='g', linestyle ='--', label="Testing Set", linewidth=2)
    plot.xlabel("Epoch")
    plot.ylabel("TPR")
    plot.legend()
    plot.savefig("Epoch_TPR({0},{1})DT.png")
    plot.show()
training()