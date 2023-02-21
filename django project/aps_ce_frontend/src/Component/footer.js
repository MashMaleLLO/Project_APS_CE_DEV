import React from "react";

const Footer = () => {
  return (
    <div className="relative w-full px-8 py-8 bg-[#FB8500] position:fixed bottom-0 left-0 right-0;">
      <div className="flex justify-between space-x-4">
        <span className="text-lg md:text-xl text-white">
          ระบบคาดการณ์ผลลัพธ์การผลิตบัณฑิตของหลักสูตรจากข้อมูลผลการเรียนของนักศึกษา{" "}
          <br />
          Curriculum output prediction from student academic data
        </span>

        <div className="flex flex-col text-white text-lg md:text-xl">
          <span>อาจารย์ที่ปรึกษา ผศ.ดร.ธนัญชัย ตรีภาค</span>
          <span>ผู้จัดทำ นางสาว ณิชกานต์ สุขุมจิตพิทโยทัย</span>
          <span className="ml-1 indent-16"> นาย นรวิชญ์ อยู่บัว</span>
        </div>
      </div>
    </div>
  );
};

export default Footer;