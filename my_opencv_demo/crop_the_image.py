	
cv::Rect rc1(rc.x1, rc.y1, rc.x2 - rc.x1, rc.y2 - rc.y1);
Mat char_img;
gray_img(rc1).copyTo(char_img);
cv::imshow("char_img", char_img);

char buf[512];
sprintf(buf, "%s/%f.jpg", save_dir.c_str(), seed);
string save_file = buf;
cv::imwrite(save_file, char_img);
