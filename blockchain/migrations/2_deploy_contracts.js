const Attendance = artifacts.require("Attendance");

module.exports = function (deployer) {
  deployer.deploy(Attendance);
};