Array.prototype.foldLeft = function (sum, callback) {
  let head,
      list = Array.prototype.slice.call(this);

  if (list.length) {
    head = list.shift(1);
    return list.foldLeft(callback(sum, head), callback);
  }
  return sum;
};

Array.prototype.foldLeftOrder = function (sum, order, callback) {
  let head,
      list = Array.prototype.slice.call(this);

  if (list.length) {
    head = list.shift(1);
    return list.foldLeftOrder(callback(sum, order, head), order + 1, callback);
  }
  return sum;
};


Array.prototype.remove = function (value) {
   return this.filter(function(ele){
       return ele != value;
   });
};

Array.prototype.add = function (value) {
  this.push(value)
  return this
};
