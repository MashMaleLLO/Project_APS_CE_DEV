import React from 'react';
import home from "../Assests/image/home.png";

function Home() {
   return (
    <div className="w-full my-4 md:py-8 md:px-32 min-h-[calc(100vh-248px)] md:min-h-[calc(100vh-158px)]">
      <div className="container mx-auto flex flex-col-reverse md:flex-row md:justify-around px-4 gap-4">
        <div className="flex flex-col justify-center space-y-6 py-6 w-full md:w-[400px]">
          <h1 className="font-bold text-3xl lg:text-4xl tracking-wide">
            ระบบคาดการณ์ผลลัพธ์การผลิตบัณฑิตของหลักสูตรจากข้อมูลผลการเรียนของนักศึกษา
          </h1>
          <p className="text-base md:text-xl font-normal leading-relaxed text-[#999999]">
            สำหรับทำนายเกรด อาชีพ แนะนำวิชาเลือกภาค โชว์สถิติอาชีพอดีตกับอนาคต
          </p>
          <div className="flex flex-col space-y-2 w-[200px]">
            <a href="https://forms.gle/kLbHKC6yuH2eZVvF9" target="_blank">
              <button
                type="submit"
                className=" text-white text-sm md:text-base px-4 py-2 rounded-lg bg-[#FF9D2E] hover:bg-[#F28204]"
              >
                กรอกข้อมูลอาชีพบัณฑิต
              </button>
            </a>
          </div>
        </div>

        <div className="flex justify-center shrink-0 overflow-hidden px-2 py-8">
          <img
            src={home}
            className="w-60 md:w-[300px] lg:w-[350px] 2xl:w-[400px]"
            alt="home"
          />
        </div>
      </div>
    </div>
  );
}

export default Home;