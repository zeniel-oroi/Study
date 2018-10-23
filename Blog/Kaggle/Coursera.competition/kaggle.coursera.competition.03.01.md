---
title: Coursera Kaggle 강의(How to win a data science competition) week 3-1 Metrics 요약
date: 2018-10-22 11:04:00
categories:
- DataScience
tags:
- DataScience
- MachineLearning
- Kaggle
---

# Coursera Kaggle 강의(How to win a data science competition) week 3-1 Metrics 요약

## Metrics

어떤 metric을 사용하느냐에 따라 모델이 학습하는 방향이 다르다. 우리가 풀고자하는 문제에 최적화된 metric을 선택하는 것이 중요하다.

### 1. Regression metrics

#### 1.1 MSE, RMSE, R-squared

- **MSE** (Mean Square Error) : target과 predict의 차이값의 제곱의 평균
  - `Best Constant` : target mean
  - `sklearn.metrics.mean_squared_error`

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.01.png)

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.02.png)

- **RMSE** (Root Mean Square Error): MSE에 root취한 값

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.03.png)

MSE의 최소값이 RMSE에서도 최소값이므로 최적화 결과가 같다. 그래서 비교적 구현이 간단한 MSE를 사용하는 경우가 많지만, **learning rate** 같은 몇몇의 hyperparameter 값에 따라 다르게 동작 할 수 있다.  
MSE와 RMSE 값이 32라고 성능이 좋은지 나쁜지 판단이 힘들다. 그래서 상대적인 값으로 평가가 필요할 수 있다.

- **R2** (R Squared)
  - `sklearn.metrics.r2_score`
  - P-Value와 같이 0 ~ 1 사이의 값을 나타내는데, MSE가 0 이면 R2는 1이며, MSE가 constant 모델보다 클 때 R2는 0이다.

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.04.png)

#### 1.2 MAE, RMAE

- **MAE** (Mean Absolute Error): target과 predict의 차이 절대값
  - `Best Constant` : target median
  - `sklearn.metrics.mean_absolute_error`

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.05.png)

- **RMAE** (Root Mean Absolute Error): MAE에 root취한 값

#### 1.3 MSE와 MAE의 차이
- MSE의 경우 차이가 2배이면 error가 4배가 되는데, MAE는 차이가 2배이면 error도 2배  
- MSE와 RMSE는 최적해를 찾기위해 gradient하게 접근시 각 지점마다 기울기(미분값)이 다르지만, MAE는 왼쪽은 -1, 오른쪽은 1이다.
- MAE는 outlier에 덜 민감하게 동작한다. (MSE는 제곱을 해서 크게 민감하다.)
- outlier가 없다고 확신이 드는 경우에는 MSE가 더 좋은 경우가 많다.

#### 1.4 (R)MSPE (Mean Square Percent Error), (R)MAPE(Mean Absolute Percent Error) : relative_metric

MSE 와 MAE는 error를 절대적인 값으로 비교를 한다. 그래서 `9 -> 10 (MAE, MSE=1)` 와 `999 -> 1000 (MAE, MSE=1)`는 같은 양의 error로 계산된다.
하지만 `900 -> 1000 (MAE=100, MSE=10000)`는 error의 수치가 훨씬 커진다. 

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.06.png)

MSPE와 MAPE는 각각 MSE와 MAE에다가 전체 데이터 개수의 퍼센트로 계산한다.

`Best Constant` 역시 MSPE는 *weighted target mean*이며, MAPE는 *weighted target median* 값이다.  
앞에 Root가 붙은 버전에 대한 설명은 생략한다.

#### 1.5 RMSLE (Root Mean Square Logarithmic Error)

- `sklearn.metrics.mean_squared_log_error`

로그 스케일로 계산된 RMSE

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.07.png)

Error 곡선의 좌우가 대칭적이지 않다.

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.08.png)

### 2. Classification metrics

#### 2.1 Accuracy
- `sklearn.metrics.accuracy_score`

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.09.png)

예측한 값과 target값이 같으면 1 아니면 0 으로 계산하여 평균을 취한 값  
개 그림 맞추기 문제에서 *개* 90, *고양이* 10으로 데이터셋이 있는 경우 모두 *개*라고 대답해도 Accuracy는 0.9가 나온다.

#### 2.2 Logarithmic loss (logloss)
- `sklearn.metrics.log_loss`

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.10.png)

target과 차이가 클수록 penalty가 커진다. 하나의 큰 error는 여러 개의 작은 error들보다 훨씬 더 penalty가 크다.

![](https://raw.githubusercontent.com/DevStarSJ/Study/master/Blog/Kaggle/Coursera.competition/image/coursera.competition.03.11.png)

#### 2.3 AUC (Area Under Curve)

얼만 구분을 잘하느냐, 얼마나 겹치는게 없느냐에 대한 검증
좋은 피처인지 아닌지를 구분할때 많이 사용
