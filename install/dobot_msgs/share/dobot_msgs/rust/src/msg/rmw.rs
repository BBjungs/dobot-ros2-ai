#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__msg__DobotAlarmCodes() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__msg__DobotAlarmCodes__init(msg: *mut DobotAlarmCodes) -> bool;
    fn dobot_msgs__msg__DobotAlarmCodes__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DobotAlarmCodes>, size: usize) -> bool;
    fn dobot_msgs__msg__DobotAlarmCodes__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DobotAlarmCodes>);
    fn dobot_msgs__msg__DobotAlarmCodes__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DobotAlarmCodes>, out_seq: *mut rosidl_runtime_rs::Sequence<DobotAlarmCodes>) -> bool;
}

// Corresponds to dobot_msgs__msg__DobotAlarmCodes
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DobotAlarmCodes {
    /// for timestamp
    pub header: std_msgs::msg::rmw::Header,

    /// list of alarm codes as hex values
    pub alarms_list: rosidl_runtime_rs::Sequence<i32>,

}



impl Default for DobotAlarmCodes {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__msg__DobotAlarmCodes__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__msg__DobotAlarmCodes__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DobotAlarmCodes {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__msg__DobotAlarmCodes__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__msg__DobotAlarmCodes__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__msg__DobotAlarmCodes__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DobotAlarmCodes {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DobotAlarmCodes where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/msg/DobotAlarmCodes";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__msg__DobotAlarmCodes() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__msg__GripperStatus() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__msg__GripperStatus__init(msg: *mut GripperStatus) -> bool;
    fn dobot_msgs__msg__GripperStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GripperStatus>, size: usize) -> bool;
    fn dobot_msgs__msg__GripperStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GripperStatus>);
    fn dobot_msgs__msg__GripperStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GripperStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<GripperStatus>) -> bool;
}

// Corresponds to dobot_msgs__msg__GripperStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GripperStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,

    /// either opened or closed
    pub status: rosidl_runtime_rs::String,

}



impl Default for GripperStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__msg__GripperStatus__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__msg__GripperStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GripperStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__msg__GripperStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__msg__GripperStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__msg__GripperStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GripperStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GripperStatus where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/msg/GripperStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__msg__GripperStatus() }
  }
}


