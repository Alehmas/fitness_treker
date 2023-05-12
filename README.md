# Fitness tracker module.

## Description
Software module for fitness tracker data processing, which calculates and displays
complete workout information based on the data from the sensor unit.

## Functionality
The module performs the following functions:
- receives information about the past training from the sensor unit
- determines the type of training
- calculates training results
- displays an information message about the training results

## Input data
The sensor unit of the fitness tracker transmits data packets in the form of a tuple,
the **first** element of which is code of the past workout, **second** - the list of indicatorsreceived from the device sensors.

### The sequence of data in the received packets:
**Swimming**
- Training code: `SWM`.
- List items: number of strokes, time in hours, user weight, pool length, how many times the user swam over the pool.

**Run**.
- Training code: `RUN`.
- List items: number of steps, training time in hours, user weight.

**Sportive Walking**
- Training code: `WLK`.
- List items: number of steps, training time in hours, user weight, user height.

*Example of input data*
```python
packages = [
     ('SWM', [720, 1, 80, 25, 40]),
     ('RUN', [15000, 1, 75]),
     ('WLK', [9000, 1, 75, 180]),
 ] 
```

## Basic Class
```python
class Training
```
**Class Properties**

* action - the main readable action during training (step - running, walking; paddling - swimming);
* duration - training duration;
* weight - athlete's weight;
* M_IN_KM = 1000 - is a constant for converting values from meters to kilometers. Its value is 1000.
* LEN_STEP - the distance the athlete covers in one step or stroke. One step is `0.65` meters,
one stroke in swimming is 1.38 meters.

**Class methods**

* get_distance() - method returns the value of the distance covered during the training
```python
# basic calculation formula
step * LEN_STEP / M_IN_KM
```
* get_mean_speed() - method returns the value of the average speed during the training
* get_spent_calories() - method returns the number of calories spent
* show_training_info() - method returns an object of the message class

## Inheritance classes
### Running training class
```python
class Running
```
**Class Properties**
inherited

**Class methods**
Overridden method:
`get_spent_calories()` - method returns the number of calories spent
```python
# calculation formula
(18 * speed - 20) * weight / M_IN_KM * duration
```

### Sportive walking Class
```python
class SportsWalking
```
**Class Properties**
Added property *height*

**Class methods**
Overridden method:
`get_spent_calories()` - method returns the number of calories spent
```python
# calculation formula
(0.035 * weight + (speed ** 2 // height) * 0.029 * weight) * duration
```

### Swimming training class
```python
class Swimming
```
**Class Properties**
Added properties:
* *length_pool* - pool length
* *count_pool* - number of pools swum

**Class methods**
Overridden method:
`get_mean_speed()` - method returns the value of the average speed during the training
```python
# calculation formula
length_pool * count_pool / M_IN_KM / duration
```
`get_spent_calories()` -method returns the number of calories spent
```python
# calculation formula
(speed + 1.1) * 2 * weight
```
## Class of information message
```python
class InfoMessage
```
**Class Properties**
* training_type - type of training
* duration - training duration
* distance - distance covered per training session
* speed - average speed of movement during movement
* calories - calories spent during the workout


**Class methods**
`get_message()` - method returns a message string:
```python
# message output
# all values of float type are rounded to 3 decimal places
'Type of training: {training_type}; Duration: {duration} h.; Distance: {distance} km; Average speed: {speed} kph; Сalories burned: {calories}'.
```

## Module functions
```python
def read_package()
```
* The read_package() function takes as input the training code and its parameter list.
* The function defines the type of training and creates an object of the corresponding class,
by passing to it the parameters received in the second argument.

```python
def main(training)
```
The `main()` function takes an instance of the `Training` class as input.
- When the `main()` function is executed, the `show_training_info()` method is called for that instance;
The result of the method should be an object of class `InfoMessage` and it should be saved in the variable `info`.
- For the `InfoMessage` object saved in the `info` variable, the method, which will return a message string with
training data; this string must be passed to the `print()` function.