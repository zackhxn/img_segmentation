default_keypoints_lefthand = [[119, 310],
       [111, 296],
       [ 98, 283],
       [ 88, 272],
       [ 79, 262],
       [ 82, 295],
       [ 67, 290],
       [ 57, 287],
       [ 47, 283],
       [ 80, 305],
       [ 63, 301],
       [ 52, 299],
       [ 43, 297],
       [ 82, 315],
       [ 66, 313],
       [ 55, 312],
       [ 45, 312],
       [ 86, 324],
       [ 75, 324],
       [ 67, 324],
       [ 60, 323]]
subtractor = 42  # 要减去的数字
subtractor2 = -54  # 要减去的数字
for i in range(len(default_keypoints_lefthand)):
    default_keypoints_lefthand[i][0] += subtractor
    default_keypoints_lefthand[i][1] += subtractor2
print(default_keypoints_lefthand)