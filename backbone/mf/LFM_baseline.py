import numpy, math, time, json, random, operator
import MF
## for each user, sample a number N of negative tags; form (user, positive tag, negative tag) combinations
## R: all triplets; P: user * K; Q: tag * K; B: tag bias vector; k: positive tag index; h: negative tag index
## initialize P, Q, B with uniform distribution
remove = ["social medium", "medium", "social", "twibe marketing", "twibe", "tweeter"]

def LFM(R, P, Q, B, K, steps=100, alpha=0.002, beta1=0.01, beta2=0.01, beta3=0.01):
    print 'start...'
    
    Q = Q.T
    step = 0

    for step in xrange(steps):
        start = time.clock()

        if step%5 == 0:
            print step
            R_shuf = []
            index_shuf = range(len(R))
            random.shuffle(index_shuf)
            for a in index_shuf:
                R_shuf.append(R[a])

        for index in xrange(len(R)):
            u, k, h = R_shuf[index]

            y_uk = B[k]+numpy.dot(P[u,:],Q[:,k])
            y_uh = B[h]+numpy.dot(P[u,:],Q[:,h])
            tmp = math.exp(y_uh-y_uk)
            e_ukh = tmp/(1+tmp)

            for i in xrange(K):
                P[u][i] = P[u][i] + alpha * (e_ukh * (Q[i][k] - Q[i][h]) - beta1 * P[u][i])
                Q[i][k] = Q[i][k] + alpha * (e_ukh * P[u][i] - beta2 * Q[i][k])
                Q[i][h] = Q[i][h] + alpha * (-e_ukh * P[u][i] - beta2 * Q[i][h])

            B[k] = B[k] + alpha * (e_ukh - beta3 * B[k])
            B[h] = B[h] + alpha * (-e_ukh - beta3 * B[h])

        
        end = time.clock()
        print 'time,',end-start
    return P, Q.T, B

class TagPred(object):
    def __init__(self):
        self.input_training = 'train-hou'
        self.input_testing = 'user_tag_dict_hou_selected'
        self.vocab = 'list-tag-hou'

    def read_input(self):
        vocab_index = {}
        index_vocab = {}
        with open(self.vocab, 'r') as f:
            for line in f:
                vocab_list = json.loads(line)

        index = 0
        for each in vocab_list:
            vocab_index[each] = index
            index_vocab[index] = each
            index += 1


        user_index = {}
        index_user = {}
        index = 0

        user_tags = {}

        R = []
        with open(self.input_training, 'r') as f:
            for line in f:
                data = json.loads(line)
                user_index[data[0]] = index
                index_user[index] = data[0]
                user_tags[data[0]] = data[1]
                

                pos_tags_dic = data[1]
                pos_tags = []
                neg_tags = []
                for tag,index1 in vocab_index.iteritems():
                    if tag in pos_tags_dic:
                        pos_tags.append(index1)
                    else:
                        neg_tags.append(index1)


                sampled_neg_tags = random.sample(neg_tags,200) #100 negative samples


                for pos_index in pos_tags:
                    for neg_index in sampled_neg_tags:
                        R.append([index, pos_index, neg_index])


                index += 1 # user index plus 1

        

        N = len(user_index)
        M = len(vocab_index)
        K = 20
        P = numpy.random.rand(N,K)
        Q = numpy.random.rand(M,K)
        B = numpy.random.rand(M,1)
        print len(R)

        P_, Q_, B_ = MF.matrix_factorization_2(R, P, Q, B, K, steps=100, alpha=0.002, beta1=0.02, beta2=0.02, beta3=0.02)
        prediction = numpy.dot(P_, Q_.T)

        for i in range(N):
            prediction[i,:] = prediction[i,:] + B_[:,0].T

        prec5 = 0.0
        count1 = 0.0
        N_test = 0
        predicted_tags = ''
        with open(self.input_testing, 'r') as f:
            for line in f:
                data = json.loads(line)
                user_id, gt = data[0], data[1]

                his_index = user_index[user_id]
                his_prediction = prediction[his_index,:]

                sorted_his_prediction = sorted(enumerate(his_prediction), key=operator.itemgetter(1), reverse=True)

                count5 = 0.0
                cnt = 0
                cnt_ = 0
                while cnt<5:
                    each = sorted_his_prediction[cnt_]
                    tag = index_vocab[each[0]]
                    cnt_ += 1
                    
                    if tag not in remove and tag not in user_tags[user_id]:
                        tg = tag.replace(' ','-')
                        predicted_tags = predicted_tags + tg + ' '

                        cnt += 1
                        if tag in gt:
                            count5 += 1

                        if tag in gt and cnt==1:
                            count1 += 1

                prec5 += count5/5


                N_test += 1

        print 'prec5:', prec5/N_test, 'prec1:', count1/N_test

        f = open('tags', 'w')
        f.write(predicted_tags)
        f.close()

if __name__=='__main__':
    tp = TagPred()
    tp.read_input()
