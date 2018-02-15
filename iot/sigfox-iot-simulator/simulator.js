const got = require('got');

String.prototype.format = function() {
  var args = arguments;
  return this.replace(/{(\d+)}/g, function(match, number) { 
    return typeof args[number] != 'undefined'
      ? args[number]
      : match
    ;
  });
};

let randomIntBetween1And = (stop) => Math.floor(Math.random() * stop) + 1;

let generatorLock = () => {
  let on = randomIntBetween1And(50) > 1 ? "1" : "0";
  let canBeUnlocked = randomIntBetween1And(30) > 1 ? "1" : "0";
  let numberOfUnlocksCurrentDay = randomIntBetween1And(10);
  let finish = toBinarySigfox(numberOfUnlocksCurrentDay,10);

  return on + canBeUnlocked + finish;
};

let generatorTemperature = () => {
  let on = randomIntBetween1And(50) > 1 ? "1" : "0";
  let temperature = toBinarySigfox(randomIntBetween1And(50),10);
  let pressure = toBinarySigfox(randomIntBetween1And(100000),20);

  return on + temperature + pressure;
};

let toBinarySigfox = (anInt,length) => {
  let binaryNumber = Number(anInt).toString(2);
  return "0".repeat(length - binaryNumber.length) + binaryNumber;
};

var devices = [
  {name:"abcdeeee",generator:generatorLock},
  {name:"eujuejjee",generator:generatorLock},
  {name:"plzllzzz",generator:generatorTemperature},
  {name:"12hhyhhee",generator:generatorTemperature}
];

const repeat = () => {
  setTimeout(async () => {
    let url = 'http://sigfox-cloud/newEvent';
    let anInteger = randomIntBetween1And(4) - 1;
    let device = devices[anInteger];
    let pattern = `deviceId: {0}
timestamp: {1}
randomMetaData: {2}
data: {3}`;
    let result = pattern.format(device["name"],Math.floor(Date.now() / 1000),randomIntBetween1And(1000000),device.generator());
    console.log(result);
    try{
      let response = await got.post(url,{body:JSON.stringify({"data":"new"})});
      console.log("Successfully joined",url);
    }catch(error){
      console.log("Unable to join",url);
    }
    repeat();
  },1000);
};

repeat();