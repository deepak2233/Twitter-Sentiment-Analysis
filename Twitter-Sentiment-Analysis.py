{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Hi everyone,\n",
    "\n",
    "* Aman Bahuguna - 18BCS2441\n",
    "* Deepak Yadav - 18BCS2446\n",
    "* Gyan Ranja - 18BCS2431"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Twitter Sentiment Analysis: Practice Problem\n",
    "### Problem Statement\n",
    "Understanding the problem statement is the first and foremost step. This would help you give an intuition of what you will face ahead of time. Let us see the problem statement -\n",
    "\n",
    "##### The objective of this task is to detect hate speech in tweets. For the sake of simplicity, we say a tweet contains hate speech if it has a racist or sexist sentiment associated with it. So, the task is to classify racist or sexist tweets from other tweets."
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "import re # for regular expressions\n",
    "import pandas as pd \n",
    "pd.set_option(\"display.max_colwidth\", 200)\n",
    "import numpy as np \n",
    "import matplotlib.pyplot as plt \n",
    "import seaborn as sns\n",
    "import string\n",
    "import nltk # for text manipulation\n",
    "import warnings \n",
    "warnings.filterwarnings(\"ignore\", category=DeprecationWarning)\n",
    "\n",
    "%matplotlib inline"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Read, Test & Train the Datasets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "train  = pd.read_csv('train_E6oV3lV.csv')\n",
    "test = pd.read_csv('test_tweets_anuFYb8.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>label</th>\n",
       "      <th>tweet</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0</td>\n",
       "      <td>@user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>0</td>\n",
       "      <td>@user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>0</td>\n",
       "      <td>bihday your majesty</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>0</td>\n",
       "      <td>#model   i love u take with u all the time in urð±!!! ðððð",
       "ð¦ð¦ð¦</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0</td>\n",
       "      <td>factsguide: society now    #motivation</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>6</td>\n",
       "      <td>0</td>\n",
       "      <td>[2/2] huge fan fare and big talking before they leave. chaos and pay disputes when they get there. #allshowandnogo</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>7</td>\n",
       "      <td>0</td>\n",
       "      <td>@user camping tomorrow @user @user @user @user @user @user @user dannyâ¦</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>8</td>\n",
       "      <td>0</td>\n",
       "      <td>the next school year is the year for exams.ð¯ can't think about that ð­ #school #exams   #hate #imagine #actorslife #revolutionschool #girl</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>9</td>\n",
       "      <td>0</td>\n",
       "      <td>we won!!! love the land!!! #allin #cavs #champions #cleveland #clevelandcavaliers  â¦</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>10</td>\n",
       "      <td>0</td>\n",
       "      <td>@user @user welcome here !  i'm   it's so #gr8 !</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   id  label  \\\n",
       "0   1      0   \n",
       "1   2      0   \n",
       "2   3      0   \n",
       "3   4      0   \n",
       "4   5      0   \n",
       "5   6      0   \n",
       "6   7      0   \n",
       "7   8      0   \n",
       "8   9      0   \n",
       "9  10      0   \n",
       "\n",
       "                                                                                                                                             tweet  \n",
       "0                                            @user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run  \n",
       "1                       @user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked  \n",
       "2                                                                                                                              bihday your majesty  \n",
       "3                                                           #model   i love u take with u all the time in urð±!!! ðððð\n",
       "ð¦ð¦ð¦    \n",
       "4                                                                                                           factsguide: society now    #motivation  \n",
       "5                             [2/2] huge fan fare and big talking before they leave. chaos and pay disputes when they get there. #allshowandnogo    \n",
       "6                                                                        @user camping tomorrow @user @user @user @user @user @user @user dannyâ¦  \n",
       "7  the next school year is the year for exams.ð¯ can't think about that ð­ #school #exams   #hate #imagine #actorslife #revolutionschool #girl  \n",
       "8                                                          we won!!! love the land!!! #allin #cavs #champions #cleveland #clevelandcavaliers  â¦   \n",
       "9                                                                                                @user @user welcome here !  i'm   it's so #gr8 !   "
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "train[train['label'] == 0].head(10)"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Text PreProcessing and Cleaning"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "Let's check out a few non racist/sexist tweets.\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>label</th>\n",
       "      <th>tweet</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>13</th>\n",
       "      <td>14</td>\n",
       "      <td>1</td>\n",
       "      <td>@user #cnn calls #michigan middle school 'build the wall' chant '' #tcot</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>14</th>\n",
       "      <td>15</td>\n",
       "      <td>1</td>\n",
       "      <td>no comment!  in #australia   #opkillingbay #seashepherd #helpcovedolphins #thecove  #helpcovedolphins</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>17</th>\n",
       "      <td>18</td>\n",
       "      <td>1</td>\n",
       "      <td>retweet if you agree!</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>23</th>\n",
       "      <td>24</td>\n",
       "      <td>1</td>\n",
       "      <td>@user @user lumpy says i am a . prove it lumpy.</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>34</th>\n",
       "      <td>35</td>\n",
       "      <td>1</td>\n",
       "      <td>it's unbelievable that in the 21st century we'd need something like this. again. #neverump  #xenophobia</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>56</th>\n",
       "      <td>57</td>\n",
       "      <td>1</td>\n",
       "      <td>@user lets fight against  #love #peace</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>68</th>\n",
       "      <td>69</td>\n",
       "      <td>1</td>\n",
       "      <td>ð©the white establishment can't have blk folx running around loving themselves and promoting our greatness</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>77</th>\n",
       "      <td>78</td>\n",
       "      <td>1</td>\n",
       "      <td>@user hey, white people: you can call people 'white' by @user  #race  #identity #medâ¦</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>82</th>\n",
       "      <td>83</td>\n",
       "      <td>1</td>\n",
       "      <td>how the #altright uses  &amp;amp; insecurity to lure men into #whitesupremacy</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>111</th>\n",
       "      <td>112</td>\n",
       "      <td>1</td>\n",
       "      <td>@user i'm not interested in a #linguistics that doesn't address #race &amp;amp; . racism is about #power. #raciolinguistics bringsâ¦</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "      id  label  \\\n",
       "13    14      1   \n",
       "14    15      1   \n",
       "17    18      1   \n",
       "23    24      1   \n",
       "34    35      1   \n",
       "56    57      1   \n",
       "68    69      1   \n",
       "77    78      1   \n",
       "82    83      1   \n",
       "111  112      1   \n",
       "\n",
       "                                                                                                                                 tweet  \n",
       "13                                                          @user #cnn calls #michigan middle school 'build the wall' chant '' #tcot    \n",
       "14                               no comment!  in #australia   #opkillingbay #seashepherd #helpcovedolphins #thecove  #helpcovedolphins  \n",
       "17                                                                                                              retweet if you agree!   \n",
       "23                                                                                     @user @user lumpy says i am a . prove it lumpy.  \n",
       "34                            it's unbelievable that in the 21st century we'd need something like this. again. #neverump  #xenophobia   \n",
       "56                                                                                             @user lets fight against  #love #peace   \n",
       "68                      ð©the white establishment can't have blk folx running around loving themselves and promoting our greatness    \n",
       "77                                             @user hey, white people: you can call people 'white' by @user  #race  #identity #medâ¦  \n",
       "82                                                       how the #altright uses  &amp; insecurity to lure men into #whitesupremacy      \n",
       "111  @user i'm not interested in a #linguistics that doesn't address #race &amp; . racism is about #power. #raciolinguistics bringsâ¦  "
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "train[train['label'] == 1].head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "((31962, 3), (17197, 2))"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "train.shape, test.shape\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0    29720\n",
       "1     2242\n",
       "Name: label, dtype: int64"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "train[\"label\"].value_counts()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAYAAAAD5CAYAAAAuneICAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADh0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uMy4xLjMsIGh0dHA6Ly9tYXRwbG90bGliLm9yZy+AADFEAAAcXUlEQVR4nO3deXRV5f3v8fdXiASUlsHoQtAbrLSLKUQIBqRJxYHRXrwVvE4/wdpSr7QOvXIFbYu3RRdtvWJZDiwqFLQMKv5Y2J9YQYRKVcAEIzJICTZLUqhEEJQCCvi9f5wn6REynCSHHA7781or6+z97Gfv8zzZcD7Zzx6OuTsiIhI9p6W6ASIikhoKABGRiFIAiIhElAJARCSiFAAiIhGlABARiajmiVQyszbAU0APwIHvA1uAZ4FsoAy41t0/MTMDfgcMAw4AY9x9XdjOaOBnYbOT3X1Obe971llneXZ2dv16JCISccXFxR+7e1Zd9SyR+wDMbA6wyt2fMrPTgVbAfcAed59iZhOAtu5+r5kNA35CLADygd+5e76ZtQOKgDxiIVIM9HH3T2p637y8PC8qKqqzfSIi8m9mVuzueXXVq3MIyMy+BhQCMwHc/Qt33wuMACr/gp8DXB2mRwBPe8xqoI2ZdQAGA8vcfU/40F8GDKlnv0REJEkSOQdwAVAB/MHM3jGzp8zsDOAcd98JEF7PDvU7Atvj1i8PZTWVi4hICiQSAM2B3sCT7n4R8C9gQi31rZoyr6X8qyubjTWzIjMrqqioSKB5IiLSEImcBC4Hyt19TZhfSCwAPjKzDu6+Mwzx7Iqrf17c+p2AHaH80mPKVx77Zu4+A5gBsXMACfdERJrU4cOHKS8v59ChQ6luSmRlZmbSqVMnMjIyGrR+nQHg7v80s+1m9i133wJcDmwKP6OBKeF1cVjlReDHZraA2EngfSEkXgEeMrO2od4gYGKDWi0iKVdeXk7r1q3Jzs4mdvGfNCV3Z/fu3ZSXl9O5c+cGbSOhy0CJXdUzN1wB9AFwC7Hho+fM7FbgQ2BUqLuE2BVApcQuA70lNHaPmf0KeDvU+6W772lQq0Uk5Q4dOqQP/xQyM9q3b09jhsoTCgB3LyF2+eaxLq+mrgPjatjOLGBWfRooIicvffinVmN//7oTWEQkohIdAhIRqVX2hJeSur2yKcOTuj05ngJA6qWh/8n1n1lOhL179zJv3jxuv/32eq03bNgw5s2bR5s2beq13uzZsxk0aBDnnntuvdZL1MqVKzn99NO55JJLTsj2j6UhIBFJW3v37uWJJ544rvzo0aO1rrdkyZJ6f/hDLAB27NhR7/UStXLlSt58880Ttv1jKQBEJG1NmDCBbdu2kZubS9++fRk4cCA33HADPXv2BODqq6+mT58+dO/enRkzZlStl52dzccff0xZWRldu3blhz/8Id27d2fQoEEcPHiw2vdauHAhRUVF3HjjjeTm5vKXv/yF733vewAsXryYli1b8sUXX3Do0CEuuOACALZt28aQIUPo06cPBQUFvP/++wBUVFRwzTXX0LdvX/r27csbb7xBWVkZ06dPZ+rUqeTm5rJq1Sqef/55evToQa9evSgsLEz6709DQCKStqZMmcKGDRsoKSlh5cqVDB8+nA0bNlRdFz9r1izatWvHwYMH6du3L9dccw3t27f/yja2bt3K/Pnz+f3vf8+1117LCy+8wE033XTce40cOZLHHnuMhx9+mLy8PI4cOcKYMWMAWLVqFT169ODtt9/myJEj5OfnAzB27FimT59Oly5dWLNmDbfffjuvvfYad955J3fffTff/va3+fDDDxk8eDCbN2/mtttu48wzz+See+4BoGfPnrzyyit07NiRvXv3Jv33pwAQkVPGxRdf/JWboqZNm8aiRYsA2L59O1u3bj0uADp37kxubi4Affr0oaysLKH3at68ORdeeCGbN29m7dq1/PSnP+X111/n6NGjFBQUsH//ft58801GjRpVtc7nn38OwKuvvsqmTZuqyj/99FM+++yz495jwIABjBkzhmuvvbbqaCOZFAAicso444wzqqZXrlzJq6++yltvvUWrVq249NJLq31sRYsWLaqmmzVrVuMQUHUKCgp4+eWXycjI4IorrmDMmDEcPXqUhx9+mC+//JI2bdpQUlJy3Hpffvklb731Fi1btqx1+9OnT2fNmjW89NJL5ObmUlJSclyANYYCQESSIhVXerVu3brav5wB9u3bR9u2bWnVqhXvv/8+q1evTvr7FRYWcvPNN3PzzTeTlZXF7t27+ec//0n37t0xMzp37szzzz/PqFGjcHfWr19Pr169GDRoEI899hjjx48HoKSkhNzcXFq3bs2nn35atf1t27aRn59Pfn4+f/rT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\n",
      "text/plain": [
       "<Figure size 432x288 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "length_train = train['tweet'].str.len()\n",
    "length_test = test['tweet'].str.len()\n",
    "\n",
    "plt.hist(length_train, bins=20, label=\"train_tweets\")\n",
    "plt.hist(length_test, bins=20, label=\"test_tweets\")\n",
    "plt.legend()\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Data Cleaning"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "(49159, 3)"
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "combi = train.append(test, ignore_index=True)\n",
    "combi.shape"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "def remove_pattern(input_txt, pattern):\n",
    "    r = re.findall(pattern, input_txt)\n",
    "    for i in r:\n",
    "        input_txt = re.sub(i, '', input_txt)\n",
    "        \n",
    "    return input_txt"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Removing Twitter Handles (@user)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>label</th>\n",
       "      <th>tweet</th>\n",
       "      <th>tidy_tweet</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run</td>\n",
       "      <td>when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked</td>\n",
       "      <td>thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>0.0</td>\n",
       "      <td>bihday your majesty</td>\n",
       "      <td>bihday your majesty</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>0.0</td>\n",
       "      <td>#model   i love u take with u all the time in urð±!!! ðððð",
       "ð¦ð¦ð¦</td>\n",
       "      <td>#model   i love u take with u all the time in urð±!!! ðððð",
       "ð¦ð¦ð¦</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0.0</td>\n",
       "      <td>factsguide: society now    #motivation</td>\n",
       "      <td>factsguide: society now    #motivation</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   id  label  \\\n",
       "0   1    0.0   \n",
       "1   2    0.0   \n",
       "2   3    0.0   \n",
       "3   4    0.0   \n",
       "4   5    0.0   \n",
       "\n",
       "                                                                                                                        tweet  \\\n",
       "0                       @user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run   \n",
       "1  @user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked   \n",
       "2                                                                                                         bihday your majesty   \n",
       "3                                      #model   i love u take with u all the time in urð±!!! ðððð\n",
       "ð¦ð¦ð¦     \n",
       "4                                                                                      factsguide: society now    #motivation   \n",
       "\n",
       "                                                                                                         tidy_tweet  \n",
       "0                   when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run  \n",
       "1    thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked  \n",
       "2                                                                                               bihday your majesty  \n",
       "3                            #model   i love u take with u all the time in urð±!!! ðððð\n",
       "ð¦ð¦ð¦    \n",
       "4                                                                            factsguide: society now    #motivation  "
      ]
     },
     "execution_count": 12,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "combi['tidy_tweet'] = np.vectorize(remove_pattern)(combi['tweet'], \"@[\\w]*\") \n",
    "combi.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### Removing Punctuations, Numbers, and Special Characters\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>label</th>\n",
       "      <th>tweet</th>\n",
       "      <th>tidy_tweet</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run</td>\n",
       "      <td>when a father is dysfunctional and is so selfish he drags his kids into his dysfunction    #run</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked</td>\n",
       "      <td>thanks for #lyft credit i can t use cause they don t offer wheelchair vans in pdx     #disapointed #getthanked</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>0.0</td>\n",
       "      <td>bihday your majesty</td>\n",
       "      <td>bihday your majesty</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>0.0</td>\n",
       "      <td>#model   i love u take with u all the time in urð±!!! ðððð",
       "ð¦ð¦ð¦</td>\n",
       "      <td>#model   i love u take with u all the time in ur</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0.0</td>\n",
       "      <td>factsguide: society now    #motivation</td>\n",
       "      <td>factsguide  society now    #motivation</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>6</td>\n",
       "      <td>0.0</td>\n",
       "      <td>[2/2] huge fan fare and big talking before they leave. chaos and pay disputes when they get there. #allshowandnogo</td>\n",
       "      <td>huge fan fare and big talking before they leave  chaos and pay disputes when they get there  #allshowandnogo</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>6</th>\n",
       "      <td>7</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user camping tomorrow @user @user @user @user @user @user @user dannyâ¦</td>\n",
       "      <td>camping tomorrow        danny</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>8</td>\n",
       "      <td>0.0</td>\n",
       "      <td>the next school year is the year for exams.ð¯ can't think about that ð­ #school #exams   #hate #imagine #actorslife #revolutionschool #girl</td>\n",
       "      <td>the next school year is the year for exams      can t think about that      #school #exams   #hate #imagine #actorslife #revolutionschool #girl</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>8</th>\n",
       "      <td>9</td>\n",
       "      <td>0.0</td>\n",
       "      <td>we won!!! love the land!!! #allin #cavs #champions #cleveland #clevelandcavaliers  â¦</td>\n",
       "      <td>we won    love the land    #allin #cavs #champions #cleveland #clevelandcavaliers</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>9</th>\n",
       "      <td>10</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user @user welcome here !  i'm   it's so #gr8 !</td>\n",
       "      <td>welcome here    i m   it s so #gr</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   id  label  \\\n",
       "0   1    0.0   \n",
       "1   2    0.0   \n",
       "2   3    0.0   \n",
       "3   4    0.0   \n",
       "4   5    0.0   \n",
       "5   6    0.0   \n",
       "6   7    0.0   \n",
       "7   8    0.0   \n",
       "8   9    0.0   \n",
       "9  10    0.0   \n",
       "\n",
       "                                                                                                                                             tweet  \\\n",
       "0                                            @user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run   \n",
       "1                       @user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked   \n",
       "2                                                                                                                              bihday your majesty   \n",
       "3                                                           #model   i love u take with u all the time in urð±!!! ðððð\n",
       "ð¦ð¦ð¦     \n",
       "4                                                                                                           factsguide: society now    #motivation   \n",
       "5                             [2/2] huge fan fare and big talking before they leave. chaos and pay disputes when they get there. #allshowandnogo     \n",
       "6                                                                        @user camping tomorrow @user @user @user @user @user @user @user dannyâ¦   \n",
       "7  the next school year is the year for exams.ð¯ can't think about that ð­ #school #exams   #hate #imagine #actorslife #revolutionschool #girl   \n",
       "8                                                          we won!!! love the land!!! #allin #cavs #champions #cleveland #clevelandcavaliers  â¦    \n",
       "9                                                                                                @user @user welcome here !  i'm   it's so #gr8 !    \n",
       "\n",
       "                                                                                                                                        tidy_tweet  \n",
       "0                                                  when a father is dysfunctional and is so selfish he drags his kids into his dysfunction    #run  \n",
       "1                                   thanks for #lyft credit i can t use cause they don t offer wheelchair vans in pdx     #disapointed #getthanked  \n",
       "2                                                                                                                              bihday your majesty  \n",
       "3                                                           #model   i love u take with u all the time in ur                                        \n",
       "4                                                                                                           factsguide  society now    #motivation  \n",
       "5                                   huge fan fare and big talking before they leave  chaos and pay disputes when they get there  #allshowandnogo    \n",
       "6                                                                                                                 camping tomorrow        danny     \n",
       "7  the next school year is the year for exams      can t think about that      #school #exams   #hate #imagine #actorslife #revolutionschool #girl  \n",
       "8                                                          we won    love the land    #allin #cavs #champions #cleveland #clevelandcavaliers        \n",
       "9                                                                                                            welcome here    i m   it s so #gr      "
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "combi['tidy_tweet'] = combi['tidy_tweet'].str.replace(\"[^a-zA-Z#]\", \" \")\n",
    "combi.head(10)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "combi['tidy_tweet'] = combi['tidy_tweet'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>id</th>\n",
       "      <th>label</th>\n",
       "      <th>tweet</th>\n",
       "      <th>tidy_tweet</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>1</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run</td>\n",
       "      <td>when father dysfunctional selfish drags kids into dysfunction #run</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>2</td>\n",
       "      <td>0.0</td>\n",
       "      <td>@user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked</td>\n",
       "      <td>thanks #lyft credit cause they offer wheelchair vans #disapointed #getthanked</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>3</td>\n",
       "      <td>0.0</td>\n",
       "      <td>bihday your majesty</td>\n",
       "      <td>bihday your majesty</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>4</td>\n",
       "      <td>0.0</td>\n",
       "      <td>#model   i love u take with u all the time in urð±!!! ðððð",
       "ð¦ð¦ð¦</td>\n",
       "      <td>#model love take with time</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>5</td>\n",
       "      <td>0.0</td>\n",
       "      <td>factsguide: society now    #motivation</td>\n",
       "      <td>factsguide society #motivation</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   id  label  \\\n",
       "0   1    0.0   \n",
       "1   2    0.0   \n",
       "2   3    0.0   \n",
       "3   4    0.0   \n",
       "4   5    0.0   \n",
       "\n",
       "                                                                                                                        tweet  \\\n",
       "0                       @user when a father is dysfunctional and is so selfish he drags his kids into his dysfunction.   #run   \n",
       "1  @user @user thanks for #lyft credit i can't use cause they don't offer wheelchair vans in pdx.    #disapointed #getthanked   \n",
       "2                                                                                                         bihday your majesty   \n",
       "3                                      #model   i love u take with u all the time in urð±!!! ðððð\n",
       "ð¦ð¦ð¦     \n",
       "4                                                                                      factsguide: society now    #motivation   \n",
       "\n",
       "                                                                      tidy_tweet  \n",
       "0             when father dysfunctional selfish drags kids into dysfunction #run  \n",
       "1  thanks #lyft credit cause they offer wheelchair vans #disapointed #getthanked  \n",
       "2                                                            bihday your majesty  \n",
       "3                                                     #model love take with time  \n",
       "4                                                 factsguide society #motivation  "
      ]
     },
     "execution_count": 15,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "\n",
    "combi.head()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Text Normalization\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "tokenized_tweet = combi['tidy_tweet'].apply(lambda x: x.split()) # tokenizing\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0                [when, father, dysfunctional, selfish, drags, kids, into, dysfunction, #run]\n",
       "1    [thanks, #lyft, credit, cause, they, offer, wheelchair, vans, #disapointed, #getthanked]\n",
       "2                                                                     [bihday, your, majesty]\n",
       "3                                                            [#model, love, take, with, time]\n",
       "4                                                          [factsguide, society, #motivation]\n",
       "Name: tidy_tweet, dtype: object"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "tokenized_tweet.head()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [],
   "source": [
    "from nltk.stem.porter import *\n",
    "stemmer = PorterStemmer()\n",
    "\n",
    "tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 19,
   "metadata": {},
   "outputs": [],
   "source": [
    "from nltk.stem.porter import *\n",
    "stemmer = PorterStemmer()\n",
    "\n",
    "tokenized_tweet = tokenized_tweet.apply(lambda x: [stemmer.stem(i) for i in x]) # stemming"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Understanding the impact of Hashtags on tweets sentiment\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [],
   "source": [
    "# function to collect hashtags\n",
    "def hashtag_extract(x):\n",
    "    hashtags = []\n",
    "    # Loop over the words in the tweet\n",
    "    for i in x:\n",
    "        ht = re.findall(r\"#(\\w+)\", i)\n",
    "        hashtags.append(ht)\n",
    "\n",
    "    return hashtags"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 22,
   "metadata": {},
   "outputs": [],
   "source": [
    "# extracting hashtags from non racist/sexist tweets\n",
    "\n",
    "HT_regular = hashtag_extract(combi['tidy_tweet'][combi['label'] == 0])\n",
    "\n",
    "# extracting hashtags from racist/sexist tweets\n",
    "HT_negative = hashtag_extract(combi['tidy_tweet'][combi['label'] == 1])\n",
    "\n",
    "# unnesting list\n",
    "HT_regular = sum(HT_regular,[])\n",
    "HT_negative = sum(HT_negative,[])"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Non-Racist/Sexist Tweets"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "a = nltk.FreqDist(HT_regular)\n",
    "d = pd.DataFrame({'Hashtag': list(a.keys()),\n",
    "                  'Count': list(a.values())})\n",
    "\n",
    "# selecting top 20 most frequent hashtags     \n",
    "d = d.nlargest(columns=\"Count\", n = 20) \n",
    "plt.figure(figsize=(16,5))\n",
    "ax = sns.barplot(data=d, x= \"Hashtag\", y = \"Count\")\n",
    "ax.set(ylabel = 'Count')\n",
    "plt.show()"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Racist/Sexist Tweets\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 24,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 1152x360 with 1 Axes>"
      ]
     },
     "metadata": {
      "needs_background": "light"
     },
     "output_type": "display_data"
    }
   ],
   "source": [
    "b = nltk.FreqDist(HT_negative)\n",
    "e = pd.DataFrame({'Hashtag': list(b.keys()), 'Count': list(b.values())})\n",
    "\n",
    "# selecting top 20 most frequent hashtags\n",
    "e = e.nlargest(columns=\"Count\", n = 20)   \n",
    "plt.figure(figsize=(16,5))\n",
    "ax = sns.barplot(data=e, x= \"Hashtag\", y = \"Count\")"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.6"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
