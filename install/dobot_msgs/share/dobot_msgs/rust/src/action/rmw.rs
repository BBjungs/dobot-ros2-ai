
#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_Goal() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_Goal__init(msg: *mut PointToPoint_Goal) -> bool;
    fn dobot_msgs__action__PointToPoint_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Goal>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Goal>);
    fn dobot_msgs__action__PointToPoint_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Goal>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_Goal {
    /// goal definition
    pub motion_type: u8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: [f64; 4],


    // This member is not documented.
    #[allow(missing_docs)]
    pub velocity_ratio: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub acceleration_ratio: f64,

}

impl PointToPoint_Goal {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVJ_XYZ: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVL_XYZ: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVJ_ANGLE: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const MOTION_TYPE_MOVL_ANGLE: u8 = 5;

}


impl Default for PointToPoint_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_Goal__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_Goal() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_Result() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_Result__init(msg: *mut PointToPoint_Result) -> bool;
    fn dobot_msgs__action__PointToPoint_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Result>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Result>);
    fn dobot_msgs__action__PointToPoint_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Result>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub achieved_pose: [f64; 4],

}



impl Default for PointToPoint_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_Result__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_Result where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_Result() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_Feedback__init(msg: *mut PointToPoint_Feedback) -> bool;
    fn dobot_msgs__action__PointToPoint_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Feedback>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Feedback>);
    fn dobot_msgs__action__PointToPoint_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_Feedback>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub current_pose: [f64; 4],

}



impl Default for PointToPoint_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_Feedback__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_Feedback() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_FeedbackMessage__init(msg: *mut PointToPoint_FeedbackMessage) -> bool;
    fn dobot_msgs__action__PointToPoint_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_FeedbackMessage>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_FeedbackMessage>);
    fn dobot_msgs__action__PointToPoint_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_FeedbackMessage>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::PointToPoint_Feedback,

}



impl Default for PointToPoint_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_FeedbackMessage() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_Goal() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_Goal__init(msg: *mut SlidingRail_Goal) -> bool;
    fn dobot_msgs__action__SlidingRail_Goal__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Goal>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_Goal__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Goal>);
    fn dobot_msgs__action__SlidingRail_Goal__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_Goal>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Goal>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_Goal
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_Goal {

    // This member is not documented.
    #[allow(missing_docs)]
    pub target_pose: f64,

}



impl Default for SlidingRail_Goal {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_Goal__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_Goal__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_Goal {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Goal__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Goal__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Goal__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_Goal {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_Goal where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_Goal";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_Goal() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_Result() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_Result__init(msg: *mut SlidingRail_Result) -> bool;
    fn dobot_msgs__action__SlidingRail_Result__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Result>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_Result__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Result>);
    fn dobot_msgs__action__SlidingRail_Result__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_Result>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Result>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_Result
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_Result {

    // This member is not documented.
    #[allow(missing_docs)]
    pub achieved_pose: f64,

}



impl Default for SlidingRail_Result {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_Result__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_Result__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_Result {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Result__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Result__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Result__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_Result {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_Result where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_Result";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_Result() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_Feedback() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_Feedback__init(msg: *mut SlidingRail_Feedback) -> bool;
    fn dobot_msgs__action__SlidingRail_Feedback__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Feedback>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_Feedback__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Feedback>);
    fn dobot_msgs__action__SlidingRail_Feedback__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_Feedback>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_Feedback>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_Feedback
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_Feedback {

    // This member is not documented.
    #[allow(missing_docs)]
    pub current_pose: f64,

}



impl Default for SlidingRail_Feedback {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_Feedback__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_Feedback__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_Feedback {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Feedback__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Feedback__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_Feedback__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_Feedback {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_Feedback where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_Feedback";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_Feedback() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_FeedbackMessage() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_FeedbackMessage__init(msg: *mut SlidingRail_FeedbackMessage) -> bool;
    fn dobot_msgs__action__SlidingRail_FeedbackMessage__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_FeedbackMessage>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_FeedbackMessage__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_FeedbackMessage>);
    fn dobot_msgs__action__SlidingRail_FeedbackMessage__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_FeedbackMessage>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_FeedbackMessage>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_FeedbackMessage
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_FeedbackMessage {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub feedback: super::super::action::rmw::SlidingRail_Feedback,

}



impl Default for SlidingRail_FeedbackMessage {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_FeedbackMessage__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_FeedbackMessage__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_FeedbackMessage {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_FeedbackMessage__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_FeedbackMessage__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_FeedbackMessage__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_FeedbackMessage {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_FeedbackMessage where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_FeedbackMessage";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_FeedbackMessage() }
  }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_SendGoal_Request__init(msg: *mut PointToPoint_SendGoal_Request) -> bool;
    fn dobot_msgs__action__PointToPoint_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Request>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Request>);
    fn dobot_msgs__action__PointToPoint_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Request>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::PointToPoint_Goal,

}



impl Default for PointToPoint_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_SendGoal_Response__init(msg: *mut PointToPoint_SendGoal_Response) -> bool;
    fn dobot_msgs__action__PointToPoint_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Response>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Response>);
    fn dobot_msgs__action__PointToPoint_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_SendGoal_Response>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for PointToPoint_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal_Response() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_GetResult_Request__init(msg: *mut PointToPoint_GetResult_Request) -> bool;
    fn dobot_msgs__action__PointToPoint_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Request>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Request>);
    fn dobot_msgs__action__PointToPoint_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Request>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for PointToPoint_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_GetResult_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__PointToPoint_GetResult_Response__init(msg: *mut PointToPoint_GetResult_Response) -> bool;
    fn dobot_msgs__action__PointToPoint_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Response>, size: usize) -> bool;
    fn dobot_msgs__action__PointToPoint_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Response>);
    fn dobot_msgs__action__PointToPoint_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<PointToPoint_GetResult_Response>) -> bool;
}

// Corresponds to dobot_msgs__action__PointToPoint_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct PointToPoint_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::PointToPoint_Result,

}



impl Default for PointToPoint_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__PointToPoint_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__PointToPoint_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for PointToPoint_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__PointToPoint_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for PointToPoint_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for PointToPoint_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/PointToPoint_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__PointToPoint_GetResult_Response() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_SendGoal_Request__init(msg: *mut SlidingRail_SendGoal_Request) -> bool;
    fn dobot_msgs__action__SlidingRail_SendGoal_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Request>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_SendGoal_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Request>);
    fn dobot_msgs__action__SlidingRail_SendGoal_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Request>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_SendGoal_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_SendGoal_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,


    // This member is not documented.
    #[allow(missing_docs)]
    pub goal: super::super::action::rmw::SlidingRail_Goal,

}



impl Default for SlidingRail_SendGoal_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_SendGoal_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_SendGoal_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_SendGoal_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_SendGoal_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_SendGoal_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_SendGoal_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_SendGoal_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_SendGoal_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_SendGoal_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_SendGoal_Response__init(msg: *mut SlidingRail_SendGoal_Response) -> bool;
    fn dobot_msgs__action__SlidingRail_SendGoal_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Response>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_SendGoal_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Response>);
    fn dobot_msgs__action__SlidingRail_SendGoal_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_SendGoal_Response>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_SendGoal_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_SendGoal_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub accepted: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub stamp: builtin_interfaces::msg::rmw::Time,

}



impl Default for SlidingRail_SendGoal_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_SendGoal_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_SendGoal_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_SendGoal_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_SendGoal_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_SendGoal_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_SendGoal_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_SendGoal_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_SendGoal_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_SendGoal_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal_Response() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_GetResult_Request() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_GetResult_Request__init(msg: *mut SlidingRail_GetResult_Request) -> bool;
    fn dobot_msgs__action__SlidingRail_GetResult_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Request>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_GetResult_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Request>);
    fn dobot_msgs__action__SlidingRail_GetResult_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Request>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_GetResult_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_GetResult_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub goal_id: unique_identifier_msgs::msg::rmw::UUID,

}



impl Default for SlidingRail_GetResult_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_GetResult_Request__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_GetResult_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_GetResult_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_GetResult_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_GetResult_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_GetResult_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_GetResult_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_GetResult_Request where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_GetResult_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_GetResult_Request() }
  }
}


#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_GetResult_Response() -> *const std::ffi::c_void;
}

#[link(name = "dobot_msgs__rosidl_generator_c")]
extern "C" {
    fn dobot_msgs__action__SlidingRail_GetResult_Response__init(msg: *mut SlidingRail_GetResult_Response) -> bool;
    fn dobot_msgs__action__SlidingRail_GetResult_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Response>, size: usize) -> bool;
    fn dobot_msgs__action__SlidingRail_GetResult_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Response>);
    fn dobot_msgs__action__SlidingRail_GetResult_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SlidingRail_GetResult_Response>) -> bool;
}

// Corresponds to dobot_msgs__action__SlidingRail_GetResult_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SlidingRail_GetResult_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub status: i8,


    // This member is not documented.
    #[allow(missing_docs)]
    pub result: super::super::action::rmw::SlidingRail_Result,

}



impl Default for SlidingRail_GetResult_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !dobot_msgs__action__SlidingRail_GetResult_Response__init(&mut msg as *mut _) {
        panic!("Call to dobot_msgs__action__SlidingRail_GetResult_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SlidingRail_GetResult_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_GetResult_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_GetResult_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { dobot_msgs__action__SlidingRail_GetResult_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SlidingRail_GetResult_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SlidingRail_GetResult_Response where Self: Sized {
  const TYPE_NAME: &'static str = "dobot_msgs/action/SlidingRail_GetResult_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__dobot_msgs__action__SlidingRail_GetResult_Response() }
  }
}






#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__PointToPoint_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct PointToPoint_SendGoal;

impl rosidl_runtime_rs::Service for PointToPoint_SendGoal {
    type Request = PointToPoint_SendGoal_Request;
    type Response = PointToPoint_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_SendGoal() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__PointToPoint_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct PointToPoint_GetResult;

impl rosidl_runtime_rs::Service for PointToPoint_GetResult {
    type Request = PointToPoint_GetResult_Request;
    type Response = PointToPoint_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__PointToPoint_GetResult() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__SlidingRail_SendGoal
#[allow(missing_docs, non_camel_case_types)]
pub struct SlidingRail_SendGoal;

impl rosidl_runtime_rs::Service for SlidingRail_SendGoal {
    type Request = SlidingRail_SendGoal_Request;
    type Response = SlidingRail_SendGoal_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_SendGoal() }
    }
}




#[link(name = "dobot_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_GetResult() -> *const std::ffi::c_void;
}

// Corresponds to dobot_msgs__action__SlidingRail_GetResult
#[allow(missing_docs, non_camel_case_types)]
pub struct SlidingRail_GetResult;

impl rosidl_runtime_rs::Service for SlidingRail_GetResult {
    type Request = SlidingRail_GetResult_Request;
    type Response = SlidingRail_GetResult_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__dobot_msgs__action__SlidingRail_GetResult() }
    }
}


