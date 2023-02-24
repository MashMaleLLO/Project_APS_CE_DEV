import React from "react";

const Footer = () => {
  return (
    <div className="w-full px-8 py-8 bg-[#FB8500] bottom-0 left-0 right-0">
      <div className="flex justify-between space-x-4">
        <span className="text-base md:text-lg text-white">
          ระบบคาดการณ์ผลลัพธ์การผลิตบัณฑิตของหลักสูตรจากข้อมูลผลการเรียนของนักศึกษา{" "}
          <br />
          Curriculum output prediction from student academic data
        </span>

        <div className="flex flex-col text-white text-base md:text-lg">
          <span>อาจารย์ที่ปรึกษา ผศ.ดร.ธนัญชัย ตรีภาค</span>
          <span>ผู้จัดทำ นางสาว ณิชกานต์ สุขุมจิตพิทโยทัย</span>
          <span className="ml-1 indent-16"> นาย นรวิชญ์ อยู่บัว</span>
        </div>
      </div>
    </div>
  );
};

export default Footer;