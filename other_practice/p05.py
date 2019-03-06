# p05

# Secret Map -- The first problem from the 2018 "Blind Recruitment" coding
# challenge administered by KakaoTalk. Though described as an "easy" problem,
# it is still important to make sure that the output is in the correct form. 
# (Ex. has the correct width and so on.) Source: https://tinyurl.com/y66fczyn.
#
# 비밀 지도 (난이도: 하)
#
# 네오는 평소 프로도가 비상금을 숨겨놓는 장소를 알려줄 비밀지도를 손에 넣었다. 
# 그런데 이 비밀지도는 숫자로 암호화되어 있어 위치를 확인하기 위해서는 암호를 
# 해독해야 한다. 다행히 지도 암호를 해독할 방법을 적어놓은 메모도 함께 발견했다.
#
#   1. 지도는 한 변의 길이가 n인 정사각형 배열 형태로, 각 칸은 “공백” 
#      (“ “) 또는 “벽”(“#”) 두 종류로 이루어져 있다.
#   2. 전체 지도는 두 장의 지도를 겹쳐서 얻을 수 있다. 각각 “지도 1”과
#      “지도 2”라고 하자. 지도 1 또는 지도 2 중 어느 하나라도 벽인 
#      부분은 전체 지도에서도 벽이다. 지도 1과 지도 2에서 모두 공백인 
#      부분은 전체 지도에서도 공백이다.
#   3. “지도 1”과 “지도 2”는 각각 정수 배열로 암호화되어 있다.
#   4. 암호화된 배열은 지도의 각 가로줄에서 벽 부분을 1, 공백 부분을 0으로
#      부호화했을 때 얻어지는 이진수에 해당하는 값의 배열이다.
#
# 네오가 프로도의 비상금을 손에 넣을 수 있도록, 비밀지도의 암호를 해독하는 
# 작업을 도와줄 프로그램을 작성하라.
#
# 입력 형식
# 입력으로 지도의 한 변 크기 n 과 2개의 정수 배열 arr1, arr2가 들어온다.
#
#   • 1 <= n <= 16
#   • arr1, arr2는 길이 n인 정수 배열로 주어진다.
#   • 정수 배열의 각 원소 x를 이진수로 변환했을 때의 길이는 n 이하이다. 즉, 
#     0 <= x <= 2^n-1을 만족한다.
#
# 출력 형식
# 원래의 비밀지도를 해독하여 "#", 공백으로 구성된 문자열 배열로 출력하라.

##############################################################################

# "지도 1 또는 지도 2 중 어느 하나라도 벽인 부분은 전체 지도에서도 벽이다"라는 
# 것으로 비트 연산인 OR를 사용하면 된다는 것을 알 수 있습니다. 코멘트는 모두 
# 영어로 작성했습니다. 

def f1(n,arr1,arr2):
    """Combines and decodes Frodo's two encoded secret maps to return 
    the rows to the true map that Neo the cat may use to find Frodo the 
    dog's stash of emergency funds.
    
    Args:
        n: An int. Guaranteed to be from 1 to 16 inclusive.
        arr1, arr2: Lists of n positive integers. Each integer can be 
          any non-negative integer that can be expressed with n bits.
        
    Returns:
        A list of n strings of length n. Strings may contain only the 
        characters "#" and " ".
    """
  
    # Python's built-in bin() function is convenient here. It converts
    # an integer to its binary representation, and we simply slice away
    # the first two characters ("0b" for all positive ints).

    return [decode(bin(x1|x2)[2:],n) for (x1,x2) in zip(arr1,arr2)]
    
def decode(bin_string,n):
    """Decodes a string to its "map" form.
    
    Args:
        bin_string: A string of length <= n consisting only of "1" and
          "0" characters.
        n: An int. The required length of the output.
        
    Returns:
        A string (left padded with " " to length n) with a "#" for 
        every "1", and " " for every "0", in bin_string. 
    """
    builder = [" " for _ in range(n-len(bin_string))]
    builder.extend(["#" if c == "1" else " " for c in bin_string])
    return "".join(builder)
    
def test():
    """Tests example inputs, including from the problem description."""

    test_inputs = [(5,[9,20,28,18,11],[30,1,21,17,28]),
                   (6,[46,33,33,22,31,50],[27,56,19,14,14,10]),
                   (3,[1,1,1],[1,2,4]),
                   (1,[0],[0])]
                  
    test_outputs = [["#####","# # #","### #","#  ##","#####"],
                    ["######","###  #","##  ##"," #### "," #####","### # "],
                    ["  #"," ##","# #"],
                    [" "]]
                    
    for i,o in zip(test_inputs,test_outputs):
        assert f1(*i) == o