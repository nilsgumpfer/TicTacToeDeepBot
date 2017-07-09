import tensorflow as tf

def build_model(board_field_size, hidden_layers, hidden_layer_size_factor):

    # Network Architecture Parameters
    n_input = board_field_size  # Input features. Count of board tales
    n_hidden = board_field_size * hidden_layer_size_factor  # hidden layer number of features
    n_classes = board_field_size  # The number of possible moves

    # tf Graph input
    x = tf.placeholder(tf.float32, [None, n_input], 'input')
    x_wins = tf.placeholder(tf.float32, (), 'x_wins')  # Statistical purpuse
    o_wins = tf.placeholder(tf.float32, (), 'o_wins')  # Statistical purpuse
    draw = tf.placeholder(tf.float32, (), 'draw')  # Statistical purpuse
    y = tf.placeholder(tf.float32, [None, n_classes], 'labels')

    # Create model
    # Hidden layer with RELU activation
    with tf.name_scope('fully_connected_1'):
        weight_1 = tf.Variable(tf.random_normal([n_input, n_hidden], stddev=0.01), name='weight')
        baias_1 = tf.Variable(tf.random_normal([n_hidden], stddev=0.01), name='baias')
        layer_1 = tf.add(tf.matmul(x, weight_1), baias_1)
        layer_out = tf.nn.relu(layer_1)

    if hidden_layers >= 2:
        # Hidden layer with RELU activation
        with tf.name_scope('fully_connected_2'):
            weight_2 = tf.Variable(tf.random_normal([n_hidden, n_hidden], stddev=0.01), name='weight')
            baias_2 = tf.Variable(tf.random_normal([n_hidden], stddev=0.01), name='baias')
            layer_2 = tf.add(tf.matmul(layer_out, weight_2), baias_2)
            layer_out = tf.nn.relu(layer_2)

    if hidden_layers >= 3:
        # Hidden layer with RELU activation
        with tf.name_scope('fully_connected_3'):
            weight_3 = tf.Variable(tf.random_normal([n_hidden, n_hidden], stddev=0.01), name='weight')
            baias_3 = tf.Variable(tf.random_normal([n_hidden], stddev=0.01), name='baias')
            layer_3 = tf.add(tf.matmul(layer_out, weight_3), baias_3)
            layer_out = tf.nn.relu(layer_3)

    # Output layer with linear activation
    with tf.name_scope('output'):
        weight_out = tf.Variable(tf.random_normal([n_hidden, n_classes], stddev=0.01), name='weight')
        baias_out = tf.Variable(tf.random_normal([n_classes], stddev=0.01), name='baias')
        out_layer = tf.matmul(layer_out, weight_out) + baias_out

    pred = out_layer

    return x, y, pred, x_wins, o_wins, draw


def save_model(session, folder, x, pred):
    saver = tf.train.Saver()
    tf.add_to_collection('input', x)
    tf.add_to_collection('pred', pred)
    saver.save(session, folder + '/model')
    saver.export_meta_graph(folder + '/model.meta')


def load_model(session, folder):
    new_saver = tf.train.import_meta_graph(folder + '/model.meta')
    new_saver.restore(session, folder + '/model')
    x = tf.get_collection('input')[0]
    pred = tf.get_collection('pred')[0]
    return x, pred