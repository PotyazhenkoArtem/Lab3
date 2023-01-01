import NemAll_Python_Geometry as G
import NemAll_Python_BaseElements as BE
import NemAll_Python_BasisElements as BEs
import GeometryValidate as GeometryValidate


def check_allplan_version(build_ele, version):
    del build_ele
    del version
    return True


def create_element(build_ele, doc):
    element = BentBeam(doc)
    return element.create(build_ele)


class BentBeam:
    def __init__(self, doc):
        self.model_ele_list = []
        self.handle_list = []
        self.document = doc

    def create(self, build_ele):
        self.beam_union(build_ele)
        self.lower_beam(build_ele)
        return (self.model_ele_list, self.handle_list)

    def beam_union(self, build_ele):
        style = BE.CommonProperties()
        style.GetGlobalProperties()
        style.Pen = 1
        style.Color = 3
        style.Stroke = 1
        down = self.lower_beam(build_ele)
        middle = self.middle_beam(build_ele)
        up = self.create_top_part_beam(build_ele)
        _, figure = G.MakeUnion(down, middle)
        if _:
            return
        _, figure = G.MakeUnion(figure, up)
        if _:
            return
        self.model_ele_list.append(
            BEs.ModelElement3D(style, figure))

    def lower_beam(self, build_ele):
        figure = self.l_part1(build_ele)
        _, figure = G.MakeUnion(figure, self.l_part2(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part3(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part4(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part2_2(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part3_2(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part4_2(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part2_3(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part3_3(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part2_4(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part3_4(build_ele))
        _, figure = G.MakeUnion(figure, self.l_part_l(build_ele))
        return figure

    def create_top_part_beam(self, build_ele):
        plus = (build_ele.BeamLength.value - build_ele.MiddleEndsWidth.value)
        figure = self.t_part1(build_ele)
        _, figure = G.MakeUnion(figure, self.t_part3(build_ele))
        _, figure = G.MakeUnion(figure, self.t_part2(build_ele))
        _, figure = G.MakeUnion(figure, self.t_part3(build_ele, plus=plus))
        _, figure = G.MakeUnion(figure, self.t_part4(build_ele))
        _, figure = G.MakeUnion(figure, self.t_part2_2(build_ele))
        _, figure = G.MakeUnion(figure, self.t_part4(build_ele, build_ele.LowerWidthSupport.value -
                                build_ele.LowerWidthSupportCut.value * 2, build_ele.TopWidthSupport.value, 10))
        _, figure = G.MakeUnion(figure, self.t_part2_3(build_ele))
        _, figure = G.MakeUnion(figure, self.t_part4_2(build_ele))
        _, figure = G.MakeUnion(figure, self.t_part4_2(build_ele, build_ele.LowerWidthSupport.value -
                                build_ele.LowerWidthSupportCut.value * 2, build_ele.TopWidthSupport.value, 10))
        _, figure = G.MakeUnion(figure, self.t_part3_3(build_ele))
        _, figure = G.MakeUnion(figure, self.t_part_l(build_ele))
        return figure

    def middle_beam(self, build_ele):
        _1 = build_ele.LowerWidthSupportCut.value
        _2 = build_ele.LowerHeightSupport.value
        _3 = build_ele.LowerWidthSupport.value
        _4 = build_ele.MiddleEndsWidth.value
        _5 = build_ele.LengthTransition.value
        _6 = build_ele.MiddleWidth.value
        _7 = build_ele.BeamLength.value
        pol = G.Polygon3D()
        pol += G.Point3D(0, _1, _2)
        pol += G.Point3D(0, _3 - _1, _2)
        pol += G.Point3D(_4, _3 - _1, _2)
        pol += G.Point3D(_4 + _5, _3 - _1 - (_3 - _1 * 2 - _6) / 2, _2)
        pol += G.Point3D(_7 - (_4 + _5), _3 - _1 - (_3 - _1 * 2 - _6) / 2, _2)
        pol += G.Point3D(_7 - _4, _3 - _1, _2)
        pol += G.Point3D(_7, _3 - _1, _2)
        pol += G.Point3D(_7, _1, _2)
        pol += G.Point3D(_7 - _4, _1, _2)
        pol += G.Point3D(_7 - _4 - _5, _1 + (_3 - _1 * 2 - _6) / 2, _2)
        pol += G.Point3D(_4 + _5, _1 + (_3 - _1 * 2 - _6) / 2, _2)
        pol += G.Point3D(_4, _1, _2)
        pol += G.Point3D(0, _1, _2)

        direction = G.Polyline3D()
        direction += G.Point3D(0, _1, _2)
        direction += G.Point3D(0, _1, _2 + build_ele.MiddleHeight.value)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part1(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        _9 = build_ele.BeamLength.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1, _2 - _3 - (_2 - _3 * 2 - _4) / 2, _5 + _6)
        pol += G.Point3D(_1, _7 - (_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_1, -(_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_1, _3 + (_2 - _3 * 2 - _4) / 2, _5 + _6)
        pol += G.Point3D(_1, _2 - _3 - (_2 - _3 * 2 - _4) / 2, _5 + _6)
        direction = G.Polyline3D()
        direction += G.Point3D(_1, _2 - _3 - (_2 - _3 * 2 - _4) / 2, _5 + _6)
        direction += G.Point3D(_9 - _1, _2 - _3 -
                               (_2 - _3 * 2 - _4) / 2, _5 + _6)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part2(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        _9 = build_ele.BeamLength.value
        _10 = build_ele.LengthTransition.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1, _2 - _3, _5 + _6)
        pol += G.Point3D(_9 - _1 - _10, _2 - _3 -
                         (_2 - _3 * 2 - _4) / 2, _5 + _6)
        pol += G.Point3D(_9 - _1 - _10 - (_2 - _3 * 2 - _4) / 2,
                         _2 - (_2 - _3 * 2 - _4) / 2 + (_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_9 - _1 - (_2 - _3 * 2 - _4) / 2,
                         _2 + (_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_9 - _1, _2 - _3, _5 + _6)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1, _2 -
                               _3, _5 + _6)
        direction += G.Point3D(_9 - _1 + 10, _2 -
                               _3 - 10, _5 + _6 + 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part3(self, build_ele, plus=0):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        pol = G.Polygon3D()
        pol += G.Point3D(plus, _3,
                         _5 + _6)
        pol += G.Point3D(plus, _2 - _3,
                         _5 + _6)
        pol += G.Point3D(plus, _2 + (_7 - _2) /
                         2, _5 + _6 + _8)
        pol += G.Point3D(plus, -(_7 - _2) / 2,
                         _5 + _6 + _8)
        pol += G.Point3D(plus, _3,
                         _5 + _6)

        direction = G.Polyline3D()
        direction += G.Point3D(plus, _3,
                               _5 + _6)
        direction += G.Point3D(plus + _1, _3,
                               _5 + _6)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part4(self, build_ele, minus_1=0, minus_2=0, digit=-10):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        _9 = build_ele.BeamLength.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1, _2 -
                         _3 - minus_1, _5 + _6)
        pol += G.Point3D(_9 - _1, _7 - (_7 -
                         _2) / 2 - minus_2, _5 + _6 + _8)
        pol += G.Point3D(_9 - _1 - (_2 - _3 * 2 - _4) / 2,
                         _2 + (_7 - _2) / 2 - minus_2, _5 + _6 + _8)
        pol += G.Point3D(_9 - _1, _2 -
                         _3 - minus_1, _5 + _6)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1, _2 -
                               _3 - minus_1, _5 + _6)
        direction += G.Point3D(_9 - _1, _2 -
                               _3 + digit - minus_1, _5 + _6)
        print(pol)
        print(direction)
        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part2_2(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        _9 = build_ele.BeamLength.value
        _10 = build_ele.LengthTransition.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1,
                         _3, _5 + _6)
        pol += G.Point3D(_9 - _1 - _10, _3 + (
            _2 - _3 * 2 - _4) / 2, _5 + _6)
        pol += G.Point3D(_9 - _1 - _10 - (_2 - _3 * 2 - _4) / 2, (_2 -
                         _3 * 2 - _4) / 2 - (_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_9 - _1 - (_2 - _3 * 2 - _4) /
                         2, -(_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_9 - _1,
                         _3, _5 + _6)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1,
                               _3, _5 + _6)
        direction += G.Point3D(_9 - _1 + 10,
                               _3 + 10, _5 + _6 + 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part2_3(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        _10 = build_ele.LengthTransition.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1, _2 -
                         _3, _5 + _6)
        pol += G.Point3D(_1 + _10, _2 - _3 - (
            _2 - _3 * 2 - _4) / 2, _5 + _6)
        pol += G.Point3D(_1 + _10 + (_2 - _3 * 2 - _4) / 2, _2 - (_2 -
                         _3 * 2 - _4) / 2 + (_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_1 + (_2 - _3 * 2 - _4) / 2, _2 +
                         (_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_1, _2 -
                         _3, _5 + _6)

        direction = G.Polyline3D()
        direction += G.Point3D(_1, _2 -
                               _3, _5 + _6)
        direction += G.Point3D(_1 - 10, _2 -
                               _3 - 10, _5 + _6 - 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part4_2(self, build_ele, minus_1=0, minus_2=0, digit=-10):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1, _2 -
                         _3 - minus_1, _5 + _6)
        pol += G.Point3D(_1, _2 + (_7 - _2) /
                         2 - minus_2, _5 + _6 + _8)
        pol += G.Point3D(_1 + (_2 - _3 * 2 - _4) / 2, _2 +
                         (_7 - _2) / 2 - minus_2, _5 + _6 + _8)
        pol += G.Point3D(_1, _2 -
                         _3 - minus_1, _5 + _6)

        direction = G.Polyline3D()
        direction += G.Point3D(_1, _2 -
                               _3 - minus_1, _5 + _6)
        direction += G.Point3D(_1, _2 -
                               _3 - minus_1 + digit, _5 + _6)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part3_3(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        _10 = build_ele.LengthTransition.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1, _3,
                         _5 + _6)
        pol += G.Point3D(_1 + _10, _3 + (_2 -
                         _3 * 2 - _4) / 2, _5 + _6)
        pol += G.Point3D(_1 + _10 + (_2 - _3 * 2 - _4) / 2, (_2 -
                         _3 * 2 - _4) / 2 - (_7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_1 + (_2 - _3 * 2 - _4) / 2, -(
            _7 - _2) / 2, _5 + _6 + _8)
        pol += G.Point3D(_1, _3,
                         _5 + _6)

        direction = G.Polyline3D()
        direction += G.Point3D(_1, _3,
                               _5 + _6)
        direction += G.Point3D(_1 - 10, _3 +
                               10, _5 + _6 - 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def t_part_l(self, build_ele):
        _2 = build_ele.LowerWidthSupport.value
        _5 = build_ele.LowerHeightSupport.value
        _6 = build_ele.MiddleHeight.value
        _7 = build_ele.TopWidthSupport.value
        _8 = build_ele.TopHeigthSupport.value
        _9 = build_ele.BeamLength.value
        _11 = build_ele.Identation.value
        pol = G.Polygon3D()
        pol += G.Point3D(0, -(_7 - _2) / 2,
                         _5 + _6 + _8)
        pol += G.Point3D(0, _7 - (_7 - _2) /
                         2, _5 + _6 + _8)
        pol += G.Point3D(0, _7 - (_7 - _2) /
                         2, _5 + _6 + _8)
        pol += G.Point3D(0, _7 - (_7 - _2) / 2 -
                         _11, _5 + _6 + _8)
        pol += G.Point3D(0, _7 - (_7 - _2) / 2 - _11,
                         _5 + _6 + _8 + build_ele.HeightPlate.value)
        pol += G.Point3D(0, - (_7 - _2) / 2 + _11,
                         _5 + _6 + _8 + build_ele.HeightPlate.value)
        pol += G.Point3D(0, - (_7 - _2) / 2 + _11,
                         _5 + _6 + _8)
        pol += G.Point3D(0, - (_7 - _2) / 2,
                         _5 + _6 + _8)
        pol += G.Point3D(0, -(_7 - _2) / 2,
                         _5 + _6 + _8)

        direction = G.Polyline3D()
        direction += G.Point3D(0, -(_7 - _2) / 2,
                               _5 + _6 + _8)
        direction += G.Point3D(_9, -(_7 - _2) /
                               2, _5 + _6 + _8)
        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part1(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _9 = build_ele.BeamLength.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1, _2, _5 - _11)
        pol += G.Point3D(_1, _2 - _3 - (_2 - _3 * 2 - _4) / 2, _5)
        pol += G.Point3D(_1, _2 - _3 - (_2 - _3 * 2 - _4) / 2 - _4, _5)
        pol += G.Point3D(_1, 0, _5 - _11)
        pol += G.Point3D(_1, _2, _5 - _11)

        direction = G.Polyline3D()
        direction += G.Point3D(_1, _2, _5 - _11)
        direction += G.Point3D(_9 - _1, _2, _5 - _11)
        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part2(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _10 = build_ele.LengthTransition.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1, _2 -
                         _3, _5)
        pol += G.Point3D(_1 + _10, _2 - _3 -
                         (_2 - _3 * 2 - _4) / 2, _5)
        pol += G.Point3D(_1 + _10 + (_2 - _3 * 2 - _4) / 2,
                         _2 - (_2 - _3 * 2 - _4) / 2, _5 - _11)
        pol += G.Point3D(_1 + (_2 - _3 * 2 -
                         _4) / 2, _2, _5 - _11)
        pol += G.Point3D(_1, _2 -
                         _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_1, _2 -
                               _3, _5)
        direction += G.Point3D(_1 - 10, _2 -
                               _3 - 10, _5 - 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part3(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _5 = build_ele.LowerHeightSupport.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(0, _2,
                         _5 - _11)
        pol += G.Point3D(0, _2 -
                         _3, _5)
        pol += G.Point3D(0, _3,
                         _5)
        pol += G.Point3D(0, 0, _5 -
                         _11)
        pol += G.Point3D(0, _2,
                         _5 - _11)

        direction = G.Polyline3D()
        direction += G.Point3D(0, _2,
                               _5 - _11)
        direction += G.Point3D(_1, _2,
                               _5 - _11)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part4(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1, _2 -
                         _3, _5)
        pol += G.Point3D(_1, _2,
                         _5 - _11)
        pol += G.Point3D(_1 + (_2 - _3 * 2 -
                         _4) / 2, _2, _5 - _11)
        pol += G.Point3D(_1, _2 -
                         _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_1, _2 -
                               _3, _5)
        direction += G.Point3D(_1, _2 -
                               _3 - 10, _5)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part2_2(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _10 = build_ele.LengthTransition.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1,
                         _3, _5)
        pol += G.Point3D(_1 + _10, _3 + (
            _2 - _3 * 2 - _4) / 2, _5)
        pol += G.Point3D(_1 + _10 + (_2 - _3 * 2 - _4) / 2,
                         (_2 - _3 * 2 - _4) / 2, _5 - _11)
        pol += G.Point3D(_1 + (_2 - _3 *
                         2 - _4) / 2, 0, _5 - _11)
        pol += G.Point3D(_1,
                         _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_1,
                               _3, _5)
        direction += G.Point3D(_1 - 10,
                               _3 + 10, _5 - 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part3_2(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _5 = build_ele.LowerHeightSupport.value
        _9 = build_ele.BeamLength.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1, _2,
                         _5 - _11)
        pol += G.Point3D(_9 - _1,
                         _2 - _3, _5)
        pol += G.Point3D(_9 - _1,
                         _3, _5)
        pol += G.Point3D(_9 - _1,
                         0, _5 - _11)
        pol += G.Point3D(_9 - _1, _2,
                         _5 - _11)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1,
                               _2, _5 - _11)
        direction += G.Point3D(_9, _2,
                               _5 - _11)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part4_2(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_1,
                         _3, _5)
        pol += G.Point3D(_1, 0,
                         _5 - _11)
        pol += G.Point3D(_1 + (_2 - _3 *
                         2 - _4) / 2, 0, _5 - _11)
        pol += G.Point3D(_1,
                         _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_1,
                               _3, _5)
        direction += G.Point3D(_1,
                               _3 + 10, _5)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part2_3(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _9 = build_ele.BeamLength.value
        _10 = build_ele.LengthTransition.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1,
                         _2 - _3, _5)
        pol += G.Point3D(_9 - _1 - _10, _2 - _3 -
                         (_2 - _3 * 2 - _4) / 2, _5)
        pol += G.Point3D(_9 - _1 - _10 - (_2 - _3 * 2 - _4) / 2,
                         _2 - (_2 - _3 * 2 - _4) / 2, _5 - _11)
        pol += G.Point3D(_9 - _1 - (_2 - _3 *
                         2 - _4) / 2, _2, _5 - _11)
        pol += G.Point3D(_9 - _1,
                         _2 - _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1,
                               _2 - _3, _5)
        direction += G.Point3D(_9 - _1 + 10,
                               _2 - _3 - 10, _5 + 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part3_3(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _9 = build_ele.BeamLength.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1,
                         _2 - _3, _5)
        pol += G.Point3D(_9 - _1, _2,
                         _5 - _11)
        pol += G.Point3D(_9 - _1 - (_2 - _3 *
                         2 - _4) / 2, _2, _5 - _11)
        pol += G.Point3D(_9 - _1,
                         _2 - _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1,
                               _2 - _3, _5)
        direction += G.Point3D(_9 - _1,
                               _2 - _3 - 10, _5)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part2_4(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _9 = build_ele.BeamLength.value
        _10 = build_ele.LengthTransition.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1,
                         _3, _5)
        pol += G.Point3D(_9 - _1 - _10, _3 + (
            _2 - _3 * 2 - _4) / 2, _5)
        pol += G.Point3D(_9 - _1 - _10 - (_2 - _3 * 2 - _4) /
                         2, (_2 - _3 * 2 - _4) / 2, _5 - _11)
        pol += G.Point3D(_9 - _1 - (_2 - _3 *
                         2 - _4) / 2, 0, _5 - _11)
        pol += G.Point3D(_9 - _1,
                         _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1,
                               _3, _5)
        direction += G.Point3D(_9 - _1 -
                               10, _3 + 10, _5 - 10)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part3_4(self, build_ele):
        _1 = build_ele.MiddleEndsWidth.value
        _2 = build_ele.LowerWidthSupport.value
        _3 = build_ele.LowerWidthSupportCut.value
        _4 = build_ele.MiddleWidth.value
        _5 = build_ele.LowerHeightSupport.value
        _9 = build_ele.BeamLength.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(_9 - _1,
                         _3, _5)
        pol += G.Point3D(_9 - _1,
                         0, _5 - _11)
        pol += G.Point3D(_9 - _1 - (_2 - _3 *
                         2 - _4) / 2, 0, _5 - _11)
        pol += G.Point3D(_9 - _1,
                         _3, _5)

        direction = G.Polyline3D()
        direction += G.Point3D(_9 - _1,
                               _3, _5)
        direction += G.Point3D(_9 - build_ele.MiddleEndsWidth.value,
                               _3 + 10, _5)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure

    def l_part_l(self, build_ele):
        _2 = build_ele.LowerWidthSupport.value
        _5 = build_ele.LowerHeightSupport.value
        _9 = build_ele.BeamLength.value
        _11 = build_ele.LowerHeightSupportCut.value
        pol = G.Polygon3D()
        pol += G.Point3D(0, 20, 0)
        pol += G.Point3D(0, _2 - 20, 0)
        pol += G.Point3D(0, _2, 20)
        pol += G.Point3D(0, _2,
                         _5 - _11)
        pol += G.Point3D(0, 0, _5 -
                         _11)
        pol += G.Point3D(0, 0, 20)
        pol += G.Point3D(0, 20, 0)

        if not GeometryValidate.is_valid(pol):
            return

        direction = G.Polyline3D()
        direction += G.Point3D(0, 20, 0)
        direction += G.Point3D(_9, 20, 0)

        _, figure = G.CreatePolyhedron(pol, direction)

        if _:
            return []

        return figure
