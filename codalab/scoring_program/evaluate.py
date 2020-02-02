#!/usr/bin/env python3
import sys
import os
import os.path
import json

input_dir = sys.argv[1]
output_dir = sys.argv[2]

submit_dir = os.path.join(input_dir, 'res')
truth_dir = os.path.join(input_dir, 'ref')

if not os.path.isdir(submit_dir):
    print("%s doesn't exist" % submit_dir)

if os.path.isdir(submit_dir) and os.path.isdir(truth_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'scores.txt')
    output_file = open(output_filename, 'wb')

    truth_file = os.path.join(truth_dir, "truth.txt")
    truth = json.load(open(truth_file, "r"))

    submission_answer_file = os.path.join(submit_dir, "answer.txt")
    submission_answer = json.load(open(submission_answer_file, "r"))

    try:
        ans = {}
        for name in truth:
            ans[name] = {"answer": truth[name]["answer"], "predict": [], "source": truth[name]["source"]}
        for name in submission_answer:
            if name in ans.keys():
                ans[name]["predict"] = submission_answer[name]

        res = [[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0, 0], [0, 0]]]
        for name in ans:
            t = ans[name]["source"]
            if len(ans[name]["answer"]) == 1:
                s = 0
            else:
                s = 1

            c = 0
            if set(ans[name]["answer"]) == set(ans[name]["predict"]):
                c = 1
            for a in range(s, 2):
                res[t][a][0] += c
                res[t][a][1] += 1
                res[2][a][0] += c
                res[2][a][1] += 1

        output_file.write("kds:%.3lf\n" % (100.0 * res[0][0][0] / res[0][0][1]))
        output_file.write("kda:%.3lf\n" % (100.0 * res[0][1][0] / res[0][1][1]))
        output_file.write("cas:%.3lf\n" % (100.0 * res[1][0][0] / res[1][0][1]))
        output_file.write("caa:%.3lf\n" % (100.0 * res[1][1][0] / res[1][1][1]))
        output_file.write("as:%.3lf\n" % (100.0 * res[2][0][0] / res[2][0][1]))
        output_file.write("aa:%.3lf\n" % (100.0 * res[2][1][0] / res[2][1][1]))

        output_file.close()

        print("kds:%.3lf\n" % (100.0 * res[0][0][0] / res[0][0][1]))
        print("kda:%.3lf\n" % (100.0 * res[0][1][0] / res[0][1][1]))
        print("cas:%.3lf\n" % (100.0 * res[1][0][0] / res[1][0][1]))
        print("caa:%.3lf\n" % (100.0 * res[1][1][0] / res[1][1][1]))
        print("as:%.3lf\n" % (100.0 * res[2][0][0] / res[2][0][1]))
        print("aa:%.3lf\n" % (100.0 * res[2][1][0] / res[2][1][1]))

    except Exception as e:
        print(e)
        raise e
